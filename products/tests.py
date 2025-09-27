# products/tests.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Category, Product

class ProductAPITests(APITestCase):
    def setUp(self):
        # Create a regular user
        self.user = User.objects.create_user(username='testuser', password='password123')
        
        # Create an admin user
        self.admin_user = User.objects.create_superuser(username='admin', password='password123', email='admin@test.com')

        self.category = Category.objects.create(name='Electronics', slug='electronics')
        self.product = Product.objects.create(
            category=self.category,
            name='Test Laptop',
            price=1200.50
        )
        self.product_list_url = reverse('product-list')
        self.product_detail_url = reverse('product-detail', kwargs={'pk': self.product.pk})

    # --- Read-Only Tests (for all user types) ---
    def test_anonymous_user_can_list_products(self):
        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_regular_user_can_list_products(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # --- Write Permission Tests ---
    def test_anonymous_user_cannot_create_product(self):
        data = {'name': 'New Gadget', 'category': self.category.pk, 'price': 99.99}
        response = self.client.post(self.product_list_url, data)
        # 401 Unauthorized for anonymous users trying to write
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_regular_user_cannot_create_product(self):
        """
        UPDATED TEST: Ensure a regular authenticated user is FORBIDDEN from creating a product.
        """
        self.client.force_authenticate(user=self.user)
        data = {'name': 'New Gadget', 'category': self.category.pk, 'price': 99.99}
        response = self.client.post(self.product_list_url, data)
        # 403 Forbidden for authenticated but non-admin users
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_user_can_create_product(self):
        """
        UPDATED TEST: Ensure an admin user CAN create a product.
        """
        self.client.force_authenticate(user=self.admin_user)
        data = {'name': 'Admin Gadget', 'category': self.category.pk, 'price': 99.99}
        response = self.client.post(self.product_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_admin_user_can_delete_product(self):
        """
        UPDATED TEST: Ensure an admin user CAN delete a product.
        """
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)