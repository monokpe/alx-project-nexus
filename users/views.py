from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView


class RegisterView(generics.CreateAPIView):
    """
    Create and register a new user.

    This endpoint is publicly accessible.
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    throttle_scope = 'auth'

class ProtectedView(APIView):
    """
    An example of a protected endpoint.
    
    Requires a valid JWT in the `Authorization: Bearer <token>` header.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Hello, you are authenticated!"})
    
class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom token obtain view with stricter rate limiting.
    """
    throttle_scope = 'auth'


from rest_framework import viewsets, permissions
from .models import Address
from .serializers import AddressSerializer
from .permissions import IsOwner

class AddressViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view and edit their addresses.
    """
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        """
        This view should return a list of all the addresses
        for the currently authenticated user.
        """
        return self.request.user.addresses.all()

    def perform_create(self, serializer):
        """
        Automatically associate the address with the current user.
        """
        serializer.save(user=self.request.user)
