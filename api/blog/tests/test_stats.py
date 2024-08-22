import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient

@pytest.fixture
def test_user(db):
    return User.objects.create_user(username='testuser', password='testpass')

@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(username='admin', password='adminpass')




@pytest.fixture
def get_access_token(client, test_user):
    url = '/account/login/'
    response = client.post(url, {'username': 'testuser', 'password': 'testpass'})
    assert response.status_code == 200
    print(response.data)
    return response.data['data']['access']

@pytest.mark.django_db
class TestStatsAPI:

    def test_get_stats(self, client,get_access_token):
        client=APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + get_access_token)
  
        # GET isteği gönderme
        response = client.get(reverse('stats'))

        # İsteğin başarılı olup olmadığını kontrol etme
        assert response.status_code == 200
        assert 'data' in response.data
        assert response.data['message'] == "Stats fetched successfully"