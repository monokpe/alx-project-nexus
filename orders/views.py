from django.db import transaction

from django.conf import settings
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
import stripe

from .models import Order, OrderItem
from .serializers import OrderSerializer, CreateOrderSerializer
from users.models import Address
from users.permissions import IsOwner
from carts.models import Cart

class OrderViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    """
    A viewset for creating and viewing orders.
    Provides `list`, `retrieve`, and `create` actions.
    """
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        """
        Users can only see their own orders.
        """
        return Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateOrderSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        """
        Create an order from the user's shopping cart.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        address_id = serializer.validated_data['address_id']
        
        try:
            cart = request.user.cart
            cart_items = cart.items.all()
            if not cart_items.exists():
                return Response({"detail": "Your cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

            shipping_address = Address.objects.get(id=address_id, user=request.user)

            with transaction.atomic():
                # Create the order
                order = Order.objects.create(
                    user=request.user,
                    shipping_address=shipping_address
                )

                total_price = 0
                order_items_to_create = []

                # Create order items from cart items
                for item in cart_items:
                    order_items_to_create.append(OrderItem(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.product.price  # Snapshot the price
                    ))
                    total_price += item.total_price
                
                OrderItem.objects.bulk_create(order_items_to_create)

                # Update the order's total price
                order.total_price = total_price
                order.save()

                # Clear the cart
                cart.items.all().delete()

            # Serialize and return the final order
            order_serializer = OrderSerializer(order)
            return Response(order_serializer.data, status=status.HTTP_201_CREATED)

        except Cart.DoesNotExist:
            return Response({"detail": "You do not have a cart."}, status=status.HTTP_400_BAD_REQUEST)
        except Address.DoesNotExist:
            return Response({"detail": "Invalid address specified."}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def create_payment_intent(self, request, pk=None):
        """
        Creates a Stripe PaymentIntent for the order.
        The frontend can use the returned client_secret to confirm the payment.
        """
        order = self.get_object()

        if order.status != Order.OrderStatus.PENDING:
            return Response(
                {"detail": "Payments can only be made for pending orders."},
                status=status.HTTP_400_BAD_REQUEST
            )

        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(order.total_price * 100),  # Amount in cents
                currency='usd',
                metadata={'order_id': order.id}
            )
            return Response({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )