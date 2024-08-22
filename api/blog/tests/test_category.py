import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from api.blog.models import Category
from rest_framework.test import APIClient

@pytest.fixture
def test_user(db):
    return User.objects.create_user(username='testuser', password='testpass')

@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(username='admin', password='adminpass')

@pytest.fixture
def test_category(db):
    return Category.objects.create(name="Test Category")

@pytest.fixture
def category_data(test_user, test_category):
    return {
        'name':'New Category'
    }

@pytest.fixture
def get_access_token(client, test_user):
    url = '/account/login/'
    response = client.post(url, {'username': 'testuser', 'password': 'testpass'})
    assert response.status_code == 200
    print(response.data)
    return response.data['data']['access']

@pytest.fixture
def get_admin_access_token(client, test_user):
    url = '/account/login/'
    response = client.post(url, {'username': 'admin', 'password': 'adminpass'})
    assert response.status_code == 200
    print('Wache ich auf',response.data)
    return response.data['data']['access']

@pytest.mark.django_db
class TestCategoryAPI:


    def test_get_categories(self, client,get_access_token):
        client=APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + get_access_token)
        # Kategori oluşturma
        Category.objects.create(name="Test Category")

        # GET isteği gönderme
        response = client.get(reverse('category'))

        # İsteğin başarılı olup olmadığını kontrol etme
        assert response.status_code == 200
        assert len(response.data['data']) == 1
        assert response.data['data'][0]['name'] == "Test Category"

    def test_create_category(self, category_data,client,get_admin_access_token):
        client=APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + get_admin_access_token)
        print(get_admin_access_token)
        # POST isteği gönderme
        response = client.post(reverse('category'), category_data)

        # Kategorinin başarılı bir şekilde oluşturulup oluşturulmadığını kontrol etme
        assert response.status_code == 200
        assert Category.objects.count() == 2
        assert Category.objects.get().name == "New Category"

    def test_create_category_unauthorized(self, client,get_access_token,category_data):
        client=APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + get_access_token)

        # POST isteği gönderme
        response = client.post(reverse('category'), category_data)

        # Kategori oluşturma isteğinin yetkisiz olup olmadığını kontrol etme
        assert response.status_code == 401
        