from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Category, Product

class ProductAPITests(APITestCase):
    """
    Test suite for the Product API endpoints.
    """

    def setUp(self):
        """
        Set up the initial data for the tests.
        This method runs before every single test function.
        """
        self.user = User.objects.create_user(username='testuser', password='testpassword123')

        self.category = Category.objects.create(name='Electronics', slug='electronics')

        self.product = Product.objects.create(
            category=self.category,
            name='Test Laptop',
            description='A high-end testing laptop.',
            price=1200.50,
            stock=15
        )

        self.product_list_url = reverse('product-list') # DRF router names this automatically
        self.product_detail_url = reverse('product-detail', kwargs={'pk': self.product.pk})

    # --- Unauthenticated User Tests ---

    def test_unauthenticated_user_can_list_products(self):
        """
        Ensure unauthenticated users can retrieve the list of products.
        """
        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], self.product.name)

    def test_unauthenticated_user_can_retrieve_product(self):
        """
        Ensure unauthenticated users can retrieve a single product's details.
        """
        response = self.client.get(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)

    def test_unauthenticated_user_cannot_create_product(self):
        """
        Ensure unauthenticated users are forbidden from creating a product.
        """
        data = {'name': 'New Gadget', 'category': self.category.pk, 'price': 99.99}
        response = self.client.post(self.product_list_url, data)
        # IsAuthenticatedOrReadOnly permission denies this
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- Authenticated User Tests ---

    def test_authenticated_user_can_create_product(self):
        """
        Ensure authenticated users CAN create a new product.
        """
        # Authenticate the client for this request
        self.client.force_authenticate(user=self.user)
        
        data = {
            'name': 'New Smartphone',
            'category': self.category.pk,
            'price': 799.99,
            'stock': 50
        }
        response = self.client.post(self.product_list_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2) 
        self.assertEqual(response.data['name'], 'New Smartphone')

    def test_authenticated_user_can_update_product(self):
        """
        Ensure authenticated users CAN update an existing product.
        """
        self.client.force_authenticate(user=self.user)
        
        updated_data = {'price': 1150.00, 'name': 'Updated Test Laptop'}
        response = self.client.patch(self.product_detail_url, updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.product.refresh_from_db()
        self.assertEqual(self.product.price, 1150.00)

    def test_authenticated_user_can_delete_product(self):
        """
        Ensure authenticated users CAN delete a product.
        """
        self.client.force_authenticate(user=self.user)
        
        response = self.client.delete(self.product_detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0) 
    
    def test_authenticated_user_cannot_create_product_with_invalid_data(self):
        """
        Ensure authenticated users cannot create a product with incomplete data.
        """
        self.client.force_authenticate(user=self.user)
        
        # Missing 'name' and 'stock' fields
        data = {'category': self.category.pk, 'price': 99.99}
        response = self.client.post(self.product_list_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check if the error message is present
        self.assertIn('name', response.data)
        