from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.test import override_settings
from unittest.mock import patch

from products.models import Product, Category
from users.models import Address
from carts.models import Cart, CartItem
from .models import Order

class OrderAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.address = Address.objects.create(user=self.user, street_address="123 Test St", city="Testville", state="TS", postal_code="12345", country="USA")
        self.category = Category.objects.create(name='Books', slug='books')
        self.product = Product.objects.create(category=self.category, name='Test Book', price=25.00)
        
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

        self.order_list_create_url = reverse('order-list')

    def test_anonymous_user_cannot_create_or_list_orders(self):
        response = self.client.get(self.order_list_create_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        data = {'address_id': self.address.pk}
        response = self.client.post(self.order_list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_order_from_cart(self):
        self.client.force_authenticate(user=self.user)
        data = {'address_id': self.address.pk}
        response = self.client.post(self.order_list_create_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check if order was created
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.total_price, 50.00) # 2 * 25.00
        
        # Check if order item was created
        self.assertEqual(order.items.count(), 1)
        order_item = order.items.first()
        self.assertEqual(order_item.product, self.product)
        self.assertEqual(order_item.price, self.product.price) # Price snapshot
        
        # Check if cart was cleared
        self.cart.refresh_from_db()
        self.assertEqual(self.cart.items.count(), 0)

    def test_cannot_create_order_with_empty_cart(self):
        self.cart.items.all().delete()
        self.client.force_authenticate(user=self.user)
        data = {'address_id': self.address.pk}
        response = self.client.post(self.order_list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_create_order_with_invalid_address(self):
        self.client.force_authenticate(user=self.user)
        data = {'address_id': 999} # Invalid ID
        response = self.client.post(self.order_list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @override_settings(STRIPE_SECRET_KEY='test_sk_123')
    @patch('stripe.PaymentIntent.create')
    def test_create_payment_intent(self, mock_stripe_create):
        # Mock the Stripe API call
        mock_stripe_create.return_value = {'client_secret': 'test_secret_123'}
        
        self.client.force_authenticate(user=self.user)
        order = Order.objects.create(user=self.user, shipping_address=self.address, total_price=100.00)
        url = reverse('order-create-payment-intent', kwargs={'pk': order.pk})
        
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['clientSecret'], 'test_secret_123')
        # Verify stripe.PaymentIntent.create was called correctly
        mock_stripe_create.assert_called_once_with(
            amount=10000, # 100.00 * 100
            currency='usd',
            metadata={'order_id': order.id}
        )