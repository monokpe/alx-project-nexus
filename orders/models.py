from django.db import models
from django.conf import settings
from products.models import Product
from users.models import Address

class Order(models.Model):
    """
    Represents a customer order.
    """
    class OrderStatus(models.TextChoices):
        PENDING = 'P', 'Pending'
        PROCESSING = 'PR', 'Processing'
        SHIPPED = 'S', 'Shipped'
        DELIVERED = 'D', 'Delivered'
        CANCELLED = 'C', 'Cancelled'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    shipping_address = models.ForeignKey(
        Address, 
        on_delete=models.PROTECT, # Prevent deleting an address that is part of an order
        related_name='orders'
    )
    status = models.CharField(
        max_length=2, 
        choices=OrderStatus.choices, 
        default=OrderStatus.PENDING
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    """
    Represents an item within an order.
    Stores a snapshot of the product's price at the time of purchase.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"