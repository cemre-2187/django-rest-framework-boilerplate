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
def blog_data(test_user, test_category):
    return {
        "title": "Test Blog",
        "content": "This is a test blog content.",
        "author": test_user.id,
        "category": test_category.name
    }

@pytest.fixture
def get_access_token(client, test_user):
    url = '/account/login/'
    response = client.post(url, {'username': 'testuser', 'password': 'testpass'})
    assert response.status_code == 200
    print(response.data)
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

    def test_create_category(self, client,get_access_token):
        client=APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + get_access_token)
        
        # POST isteği gönderme
        response = client.post(reverse('category'), self.category_data)

        # Kategorinin başarılı bir şekilde oluşturulup oluşturulmadığını kontrol etme
        assert response.status_code == 200
        assert Category.objects.count() == 1
        assert Category.objects.get().name == "New Category"

    def test_create_category_unauthorized(self, client):
        # Normal kullanıcıyı giriş yapmış gibi ayarla
        client.login(username='testuser', password='testpass')

        # POST isteği gönderme
        response = client.post(reverse('category'), self.category_data)

        # Kategori oluşturma isteğinin yetkisiz olup olmadığını kontrol etme
        assert response.status_code == 401
        assert Category.objects.count() == 0