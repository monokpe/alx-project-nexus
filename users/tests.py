from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Address

class UserAddressAPITests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')

        self.address1 = Address.objects.create(
            user=self.user1,
            street_address="123 Main St",
            city="Anytown",
            state="Anystate",
            postal_code="12345",
            country="USA"
        )
        
        self.address_list_url = reverse('address-list')
        self.address_detail_url = reverse('address-detail', kwargs={'pk': self.address1.pk})

    def test_anonymous_user_cannot_access_addresses(self):
        """Ensure anonymous users are blocked.
        """
        response = self.client.get(self.address_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_create_address(self):
        """Ensure an authenticated user can create an address for themselves.
        """
        self.client.force_authenticate(user=self.user1)
        data = {
            "street_address": "456 Oak Ave",
            "city": "Someville",
            "state": "Somesota",
            "postal_code": "54321",
            "country": "USA"
        }
        response = self.client.post(self.address_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.user1.addresses.count(), 2)

    def test_user_can_list_own_addresses(self):
        """Ensure a user can list their own addresses, and only their own.
        """
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.address_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['street_address'], self.address1.street_address)

    def test_user_cannot_access_another_users_address(self):
        """Ensure a user gets a 404 when trying to access another user's address.
        """
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(self.address_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_address(self):
        """Ensure a user can update their own address.
        """
        self.client.force_authenticate(user=self.user1)
        data = {'city': 'New City'}
        response = self.client.patch(self.address_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.address1.refresh_from_db()
        self.assertEqual(self.address1.city, 'New City')

    def test_user_can_delete_own_address(self):
        """Ensure a user can delete their own address.
        """
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(self.address_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.user1.addresses.count(), 0)