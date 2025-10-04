from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.

    The `user` field is read-only and populated from the request user.
    The `product` is also read-only in the serializer as it's determined by the URL.
    """
    user = serializers.ReadOnlyField(source='user.username')
    product = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = Review
        fields = ('id', 'user', 'product', 'rating', 'comment', 'created_at')
        read_only_fields = ('created_at',)

    def validate(self, data):
        """
        Check that the user has not already reviewed this product.
        """
        if self.instance:
            # For updates, no need to check again
            return data

        user = self.context['request'].user
        product = self.context['view'].get_product_object()

        if Review.objects.filter(product=product, user=user).exists():
            raise serializers.ValidationError("You have already reviewed this product.")
        
        return data
