from django.contrib import admin
from .models import Address

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'street_address', 'city', 'country', 'is_default')
    list_filter = ('is_default', 'country')
    search_fields = ('user__username', 'street_address', 'city', 'country', 'postal_code')