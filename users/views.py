from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response


class RegisterView(generics.CreateAPIView):
    """
    Create and register a new user.

    This endpoint is publicly accessible.
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

class ProtectedView(APIView):
    """
    An example of a protected endpoint.
    
    Requires a valid JWT in the `Authorization: Bearer <token>` header.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Hello, you are authenticated!"})
    
