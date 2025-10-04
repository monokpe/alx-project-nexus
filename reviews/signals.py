from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from .models import Review

@receiver([post_save, post_delete], sender=Review)
def update_product_rating(sender, instance, **kwargs):
    """
    Signal handler to update the average rating and review count on the Product model
    whenever a Review is saved or deleted.
    """
    product = instance.product
    reviews = product.reviews.all()
    
    if reviews.exists():
        product.review_count = reviews.count()
        # Ensure the result from aggregate is not None before saving
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        product.average_rating = round(avg_rating, 2)
    else:
        product.review_count = 0
        product.average_rating = 0.00
        
    product.save()
