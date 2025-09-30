from django.contrib import admin
from .models import Category, Product
from rangefilter.filters import NumericRangeFilter
import reversion.admin

@admin.register(Category)
class CategoryAdmin(reversion.admin.VersionAdmin):
    """
    Customization for the Category model in the Django admin panel.
    """
    list_display = ('name', 'slug')
    # Automatically creates the slug from the name field
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(reversion.admin.VersionAdmin):
    """
    Customization for the Product model in the Django admin panel.
    """
    list_display = ('name', 'category', 'price', 'stock', 'created_at')
    list_filter = (('price', NumericRangeFilter), 'category', 'created_at')
    search_fields = ('name', 'description')
    list_select_related = ('category',)
    readonly_fields = ('created_at', 'updated_at')