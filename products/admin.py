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
    list_select_related = ('category',)
    readonly_fields = ('created_at', 'updated_at')

    def mark_as_in_stock(self, request, queryset):
        queryset.update(stock=100)
        self.message_user(request, "Selected products have been marked as in stock.")

    mark_as_in_stock.short_description = "Mark selected products as in stock (100 units)"

    def mark_as_out_of_stock(self, request, queryset):
        queryset.update(stock=0)
        self.message_user(request, "Selected products have been marked as out of stock.")

    mark_as_out_of_stock.short_description = "Mark selected products as out of stock"

    actions = [mark_as_in_stock, mark_as_out_of_stock]
    