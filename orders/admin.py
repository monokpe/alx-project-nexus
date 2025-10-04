from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    """
    Inline admin descriptor for OrderItem model.
    Allows viewing of order items directly within the Order admin page.
    """
    model = OrderItem
    extra = 0  # No extra forms by default
    readonly_fields = ('product', 'quantity', 'price')
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin View for Order model.
    """
    list_display = ('id', 'user', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'user__username', 'shipping_address__street_address')
    readonly_fields = ('user', 'shipping_address', 'total_price', 'created_at', 'updated_at')
    inlines = [OrderItemInline]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        # Optional: prevent deletion of orders from the admin
        return False