from rest_framework import serializers
from .models import Order, OrderItem
from users.models import Address
from products.models import Product


class SimpleProductSerializer(serializers.ModelSerializer):
    """
    A simple read-only serializer for product details in an order item.
    """
    class Meta:
        model = Product
        fields = ('id', 'name')
        read_only_fields = fields


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the OrderItem model.
    """
    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'quantity', 'price')


class SimpleAddressSerializer(serializers.ModelSerializer):
    """
    A simple read-only serializer for shipping address details.
    """
    class Meta:
        model = Address
        fields = ('street_address', 'city', 'state', 'postal_code', 'country')
        read_only_fields = fields


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model, for retrieving order details.
    """
    items = OrderItemSerializer(many=True, read_only=True)
    shipping_address = SimpleAddressSerializer(read_only=True)
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Order
        fields = (
            'id', 'user', 'shipping_address', 'status', 
            'total_price', 'created_at', 'items'
        )


class CreateOrderSerializer(serializers.Serializer):
    """
    Serializer for creating an order from a shopping cart.
    Requires the ID of a valid user address for shipping.
    """
    address_id = serializers.IntegerField()

    def validate_address_id(self, value):
        """
        Check that the address exists and belongs to the current user.
        """
        user = self.context['request'].user
        if not Address.objects.filter(pk=value, user=user).exists():
            raise serializers.ValidationError("Invalid address ID provided.")
        return value
