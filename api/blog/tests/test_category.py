import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from api.blog.models import Category
from rest_framework.test import APIClient
from api.core.tests.text_client import BaseTestClient


# @pytest.fixture
# def admin_user(db):
#     return User.objects.create_superuser(username='admin', password='adminpass')

# @pytest.fixture
# def test_user(db):
#     return User.objects.create_user(username='testuser', password='testpass')

# @pytest.fixture
# def test_category(db):
#     return Category.objects.create(name="Test Category")

# @pytest.fixture
# def category_data():
#     return {
#         'name':'New Category'
#     }

# @pytest.fixture
# def get_access_token(client, test_user):
#     url = '/account/login/'
#     response = client.post(url, {'username': 'testuser', 'password': 'testpass'})
#     assert response.status_code == 200
#     return response.data['data']['access']

# @pytest.fixture
# def get_admin_access_token(client, admin_user):
#     url = '/account/login/'
#     response = client.post(url, {'username': 'admin', 'password': 'adminpass'})
#     print(response.data)
#     assert response.status_code == 200
#     return response.data['data']['access']

@pytest.mark.django_db
class TestCategoryAPI(BaseTestClient):


    def test_get_categories(self):
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.get_admin_access_token)
        # Kategori oluşturma
        Category.objects.create(name="Test Category")

        # GET isteği gönderme
        response = self.client.get(reverse('category'))

        # İsteğin başarılı olup olmadığını kontrol etme
        assert response.status_code == 200
        assert len(response.data['data']) == 2
        assert response.data['data'][0]['name'] == "Test Category"

#     def test_create_category(self, category_data,client,get_admin_access_token,admin_user):
#         client=APIClient()
#         client.credentials(HTTP_AUTHORIZATION='Bearer ' + get_admin_access_token)
        
#         # POST isteği gönderme
#         response = client.post(reverse('category'), {
#         'name':'New Category'
#         })
#         print(response)
        
#         # Kategorinin başarılı bir şekilde oluşturulup oluşturulmadığını kontrol etme
#         assert response.status_code == 200
#         assert Category.objects.count() == 1
#         assert Category.objects.get().name == "New Category"

#     def test_create_category_unauthorized(self, client,get_access_token,category_data):
#         client=APIClient()
#         client.credentials(HTTP_AUTHORIZATION='Bearer ' + get_access_token)

#         # POST isteği gönderme
#         response = client.post(reverse('category'), category_data)

#         # Kategori oluşturma isteğinin yetkisiz olup olmadığını kontrol etme
#         assert response.status_code == 401
        