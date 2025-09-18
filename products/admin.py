from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Customization for the Category model in the Django admin panel.
    """
    list_display = ('name', 'slug')
    # Automatically creates the slug from the name field
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Customization for the Product model in the Django admin panel.
    """
    list_display = ('name', 'category', 'price', 'stock', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')
    # This is a performance optimization for the list view
    list_select_related = ('category',)
    # Makes date fields read-only
    readonly_fields = ('created_at', 'updated_at')
    