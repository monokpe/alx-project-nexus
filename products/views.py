import logging
from rest_framework import viewsets, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.urls import reverse
from django.core.cache import cache
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .permissions import IsAdminOrReadOnly

logger = logging.getLogger(__name__)

class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing product categories.
    
    Provides `list`, `create`, `retrieve`, `update`, and `destroy` actions.
    - **GET /api/v1/categories/**: List all categories.
    - **POST /api/v1/categories/**: Create a new category (Admin only).
    - **GET /api/v1/categories/{id}/**: Retrieve a specific category.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing products.
    
    This viewset provides full CRUD functionality for products and supports
    powerful filtering, searching, and sorting capabilities.
    
    ### Query Parameters:
    - `category__slug` (string): Filter products by the slug of their category.
    - `price__gte` (decimal): Filter for products with a price greater than or equal to this value.
    - `price__lte` (decimal): Filter for products with a price less than or equal to this value.
    - `search` (string): Search for products by name or description.
    - `ordering` (string): Sort the results. Available fields: `name`, `price`, `created_at`. 
      (e.g., `?ordering=price` for ascending, `?ordering=-price` for descending).
    """
    queryset = Product.objects.all().select_related('category')
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'category__slug': ['exact'],
        'price': ['gte', 'lte'],
    }
    
    search_fields = ['name', 'description']
    
    ordering_fields = ['name', 'price', 'created_at']

    def list(self, request, *args, **kwargs):
        cache_key = request.build_absolute_uri()
        cached_response = cache.get(cache_key)

        if cached_response:
            logger.info(f"Returning cached response for: {cache_key}")
            return Response(cached_response)

        logger.info(f"No cache found for: {cache_key}. Generating new response.")
        response = super().list(request, *args, **kwargs)
        
        # Cache the response data for 1 minute (60 seconds)
        cache.set(cache_key, response.data, timeout=60)
        
        logger.info(f"Product list viewed by user: {request.user}")
        return response
    
    def create(self, request, *args, **kwargs):
        logger.warning(f"Product creation attempt by user: {request.user}")
        return super().create(request, *args, **kwargs)



def redirect_to_products_by_category(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    url = reverse('admin:products_product_changelist')
    return redirect(f'{url}?category__id__exact={category.id}')


class ProductCategoryChartView(TemplateView):
    template_name = 'products/chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['labels'] = [category.name for category in Category.objects.all()]
        context['data'] = [category.products.count() for category in Category.objects.all()]
        context['provider'] = "Products"
        return context