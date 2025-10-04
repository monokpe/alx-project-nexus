from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from products.models import Category, Product
from .models import Cart, CartItem
from decimal import Decimal

class CartAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.category = Category.objects.create(name='Books', slug='books')
        self.product1 = Product.objects.create(category=self.category, name='Test Book 1', price=10.00)
        self.product2 = Product.objects.create(category=self.category, name='Test Book 2', price=15.00)

        self.cart_url = reverse('cart-detail')
        self.cart_items_url = reverse('cart-item-list')

    def test_anonymous_user_cannot_access_cart(self):
        response = self.client.get(self.cart_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_cart_creates_it_if_not_exists(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.cart_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Cart.objects.filter(user=self.user).exists())
        self.assertEqual(response.data['items'], [])

    def test_add_item_to_cart(self):
        self.client.force_authenticate(user=self.user)
        data = {'product_id': self.product1.pk, 'quantity': 2}
        response = self.client.post(self.cart_items_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 1)
        self.assertEqual(cart.items.first().quantity, 2)
        self.assertEqual(response.data['total_price'], Decimal("20.00"))

    def test_add_existing_item_to_cart_updates_quantity(self):
        self.client.force_authenticate(user=self.user)
        # Add product1 first time
        CartItem.objects.create(cart=Cart.objects.create(user=self.user), product=self.product1, quantity=1)
        
        # Add product1 second time
        data = {'product_id': self.product1.pk, 'quantity': 3}
        response = self.client.post(self.cart_items_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 1)
        self.assertEqual(cart.items.first().quantity, 4) # 1 + 3

    def test_update_cart_item_quantity(self):
        self.client.force_authenticate(user=self.user)
        cart = Cart.objects.create(user=self.user)
        item = CartItem.objects.create(cart=cart, product=self.product1, quantity=2)
        
        update_url = reverse('cart-item-detail', kwargs={'pk': item.pk})
        data = {'quantity': 5}
        response = self.client.patch(update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        item.refresh_from_db()
        self.assertEqual(item.quantity, 5)

    def test_remove_cart_item(self):
        self.client.force_authenticate(user=self.user)
        cart = Cart.objects.create(user=self.user)
        item = CartItem.objects.create(cart=cart, product=self.product1, quantity=1)
        
        delete_url = reverse('cart-item-detail', kwargs={'pk': item.pk})
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(cart.items.count(), 0)