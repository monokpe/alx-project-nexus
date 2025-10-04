from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from products.models import Category, Product
from .models import Review

class ReviewAPITests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')
        self.category = Category.objects.create(name='Electronics', slug='electronics')
        self.product = Product.objects.create(category=self.category, name='Test Laptop', price=1200.50)
        
        self.review1 = Review.objects.create(product=self.product, user=self.user1, rating=5, comment="Great!")

        self.list_create_url = reverse('review-list', kwargs={'product_pk': self.product.pk})
        self.detail_url = reverse('review-detail', kwargs={'product_pk': self.product.pk, 'pk': self.review1.pk})

    def test_anonymous_user_can_list_reviews(self):
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_anonymous_user_cannot_create_review(self):
        data = {"rating": 4, "comment": "Good"}
        response = self.client.post(self.list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_create_review(self):
        self.client.force_authenticate(user=self.user2)
        data = {"rating": 4, "comment": "Good"}
        response = self.client.post(self.list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.product.reviews.count(), 2)

    def test_user_cannot_create_duplicate_review(self):
        self.client.force_authenticate(user=self.user1) # user1 already has a review
        data = {"rating": 3, "comment": "Okay"}
        response = self.client.post(self.list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_update_own_review(self):
        self.client.force_authenticate(user=self.user1)
        data = {"rating": 4, "comment": "Updated comment"}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.review1.refresh_from_db()
        self.assertEqual(self.review1.rating, 4)

    def test_user_cannot_update_others_review(self):
        self.client.force_authenticate(user=self.user2)
        data = {"rating": 1}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_rating_signal_updates_product_on_create(self):
        self.product.refresh_from_db()
        self.assertEqual(self.product.review_count, 1)
        self.assertEqual(self.product.average_rating, 5.00)

        # Create a second review
        Review.objects.create(product=self.product, user=self.user2, rating=3)
        self.product.refresh_from_db()
        self.assertEqual(self.product.review_count, 2)
        self.assertEqual(self.product.average_rating, 4.00) # (5+3)/2

    def test_rating_signal_updates_product_on_delete(self):
        self.review1.delete()
        self.product.refresh_from_db()
        self.assertEqual(self.product.review_count, 0)
        self.assertEqual(self.product.average_rating, 0.00)