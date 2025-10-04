from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, ProtectedView, AddressViewSet

router = DefaultRouter()
router.register(r'addresses', AddressViewSet, basename='address')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('', include(router.urls)),
]
