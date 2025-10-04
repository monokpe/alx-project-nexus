from django.db import models
from django.conf import settings

class Address(models.Model):
    """
    Represents a shipping or billing address for a user.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)

    class Meta:
        ordering = ('-is_default', 'id')
        verbose_name_plural = "Addresses"
        unique_together = ('user', 'street_address', 'city', 'state', 'postal_code', 'country')

    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.country}"