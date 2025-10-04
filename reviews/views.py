from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404

from .models import Review
from .serializers import ReviewSerializer
from .permissions import IsAuthorOrReadOnly
from products.models import Product

class ReviewViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing, creating, and managing product reviews.
    Nested under /api/v1/products/{product_id}/reviews/
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_product_object(self):
        """
        Helper method to get the product object from the URL's product_pk.
        """
        return get_object_or_404(Product, pk=self.kwargs['product_pk'])

    def get_queryset(self):
        """
        This view should return a list of all the reviews for the product
        determined by the product_pk portion of the URL.
        """
        product = self.get_product_object()
        return product.reviews.all()

    def get_serializer_context(self):
        """
        Pass the product object to the serializer context.
        """
        context = super().get_serializer_context()
        context['view'] = self
        return context

    def perform_create(self, serializer):
        """
        Create a review for the product determined by the URL,
        with the user from the request.
        """
        product = self.get_product_object()
        serializer.save(user=self.request.user, product=product)