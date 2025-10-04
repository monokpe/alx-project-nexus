from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    """
    Inline admin descriptor for CartItem model.
    Allows editing of cart items directly within the Cart admin page.
    """
    model = CartItem
    extra = 1  # Number of extra forms to display
    readonly_fields = ('total_price',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """
    Admin View for Cart model.
    """
    list_display = ('user', 'created_at', 'total_price')
    readonly_fields = ('user', 'created_at', 'total_price')
    inlines = [CartItemInline]

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """
    Admin View for CartItem model (for individual access).
    """
    list_display = ('cart', 'product', 'quantity', 'total_price')
    readonly_fields = ('total_price',)