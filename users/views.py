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
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Hello, you are authenticated!"})
    
class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom token obtain view with stricter rate limiting.
    """
    throttle_scope = 'auth'

