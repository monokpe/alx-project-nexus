from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Product


class SimpleProductSerializer(serializers.ModelSerializer):
    """
    A simple serializer for products to be nested in cart items.
    """
    class Meta:
        model = Product
        fields = ('id', 'name', 'price')


class CartItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the CartItem model.
    """
    product = SimpleProductSerializer()
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'quantity', 'total_price')


class CartSerializer(serializers.ModelSerializer):
    """
    Serializer for the Cart model, with nested items and total price.
    """
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = ('id', 'user', 'items', 'total_price', 'created_at')
        read_only_fields = ('user', 'created_at')


class AddCartItemSerializer(serializers.ModelSerializer):
    """
    Serializer for adding items to a cart. Validates product existence
    and quantity.
    """
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("No product with the given ID was found.")
        return value

    class Meta:
        model = CartItem
        fields = ('product_id', 'quantity')


class UpdateCartItemSerializer(serializers.ModelSerializer):
    """
    Serializer for updating the quantity of an item in the cart.
    """
    class Meta:
        model = CartItem
        fields = ('quantity',)
