from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Item
from rest_framework_simplejwt.tokens import RefreshToken

class ItemTests(APITestCase):

    def setUp(self):
        # Create a test user and generate JWT token
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = str(RefreshToken.for_user(self.user).access_token)
        
        # Set the token for authentication
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
        # Create an item for testing purposes
        self.item = Item.objects.create(name="Test Item", description="Test Description")

    # Test item creation
    def test_create_item(self):
        url = reverse('create-item')  # URL for item creation
        data = {"name": "New Item", "description": "New Description"}
        
        # Send POST request
        response = self.client.post(url, data, format='json')
        
        # Check if item is created successfully
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "New Item")

    # Test item retrieval (detail view)
    def test_get_item(self):
        url = reverse('detail-item', kwargs={'pk': self.item.pk})
        
        # Send GET request
        response = self.client.get(url)
        
        # Check if the response is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Test Item")

    # Test item update
    def test_update_item(self):
        url = reverse('update-item', kwargs={'pk': self.item.pk})
        data = {"name": "Updated Item", "description": "Updated Description"}
        
        # Send PUT request
        response = self.client.put(url, data, format='json')
        
        # Check if the item is updated successfully
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Updated Item")

    # Test item deletion
    def test_delete_item(self):
        url = reverse('delete-item', kwargs={'pk': self.item.pk})
        
        # Send DELETE request
        response = self.client.delete(url)
        
        # Check if the item is deleted successfully
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify item is no longer in the database
        self.assertFalse(Item.objects.filter(pk=self.item.pk).exists())
