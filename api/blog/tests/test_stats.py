import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from api.core.tests.text_client import BaseTestClient

@pytest.mark.django_db
class TestStatsAPI(BaseTestClient):

    def test_get_stats(self):
        # Login for the test user
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.get_access_token)
  
        # Send a GET request
        response = self.client.get(reverse('stats'))

        # Check if the request was successful
        assert response.status_code == 200
        assert 'data' in response.data
        assert response.data['message'] == "Stats fetched successfully"