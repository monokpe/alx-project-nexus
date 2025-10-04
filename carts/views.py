from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Cart, CartItem
from .serializers import (
    CartSerializer, 
    CartItemSerializer, 
    AddCartItemSerializer, 
    UpdateCartItemSerializer
)

class CartViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    A viewset for retrieving the current user's cart.
    Provides a single endpoint to `GET` the cart.
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Retrieve (or create) the cart for the authenticated user.
        """
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

class CartItemViewSet(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """
    A viewset for managing items within a user's cart.
    Provides `create` (add), `update`, `partial_update`, and `destroy` (remove) actions.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the cart items
        for the currently authenticated user's cart.
        """
        return CartItem.objects.filter(cart__user=self.request.user)

    def get_serializer_class(self):
        """
        Return different serializers for different actions.
        """
        if self.action == 'create':
            return AddCartItemSerializer
        if self.action in ['update', 'partial_update']:
            return UpdateCartItemSerializer
        return CartItemSerializer

    def create(self, request, *args, **kwargs):
        """
        Add an item to the cart, or update its quantity if it already exists.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']

        cart, _ = Cart.objects.get_or_create(user=request.user)
        
        # Check if the item is already in the cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, 
            product_id=product_id,
            defaults={'quantity': quantity}
        )

        # If the item was not created, it means it already existed, so we update the quantity
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        # Return the state of the entire cart
        cart_serializer = CartSerializer(cart)
        return Response(cart_serializer.data, status=status.HTTP_201_CREATED)