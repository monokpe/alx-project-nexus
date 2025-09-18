from django.urls import path
from .views import RegisterView, ProtectedView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('protected/', ProtectedView.as_view(), name='protected'),
]

