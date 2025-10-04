import uuid
from django.db import models
from django.conf import settings
from products.models import Product

class Cart(models.Model):
    """
    Represents a user's shopping cart.
    Each user has one cart, created on-demand.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

    @property
    def total_price(self):
        """
        Calculates the total price of all items in the cart.
        """
        return sum(item.total_price for item in self.items.all())

class CartItem(models.Model):
    """
    Represents a product item within a user's shopping cart.
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        # Ensures a product only appears once in a cart.
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in cart for {self.cart.user.username}"

    @property
    def total_price(self):
        """
        Calculates the total price for this cart item.
        """
        return self.product.price * self.quantity