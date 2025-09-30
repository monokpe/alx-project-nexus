import logging # Import the logging library at the top
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .permissions import IsAdminOrReadOnly
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework_extensions.key_constructor.constructors import DefaultListKeyConstructor
from rest_framework_extensions.key_constructor import bits

# Import the caching mixin


# Get an instance of a logger
logger = logging.getLogger(__name__)

class CustomListKeyConstructor(DefaultListKeyConstructor):
    query_params = bits.QueryParamsKeyBit()

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

class ProductViewSet(CacheResponseMixin, viewsets.ModelViewSet):
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
    list_cache_key_func = CustomListKeyConstructor()
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'category__slug': ['exact'],
        'price': ['gte', 'lte'],
    }
    
    search_fields = ['name', 'description']
    
    ordering_fields = ['name', 'price', 'created_at']

    def list(self, request, *args, **kwargs):
        # Add a log message to the list method
        logger.info(f"Product list viewed by user: {request.user}")
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        # Add a log message to the create method
        logger.warning(f"Product creation attempt by user: {request.user}")
        return super().create(request, *args, **kwargs)