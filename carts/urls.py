from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartViewSet, CartItemViewSet

router = DefaultRouter()
router.register(r'items', CartItemViewSet, basename='cart-item')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    # Route for the singleton cart view
    path('', CartViewSet.as_view({'get': 'retrieve'}), name='cart-detail'),
    # Routes for cart items (e.g., /cart/items/, /cart/items/{item_pk}/)
    path('', include(router.urls)),
]
