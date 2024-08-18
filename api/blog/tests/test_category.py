import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from api.blog.models import Category

@pytest.mark.django_db
class TestCategoryAPI:

    @pytest.fixture(scope='class')
    def setup_class(self, db):
        # Test için gerekli kullanıcıyı oluşturma
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpass')
        self.category_data = {"name": "New Category"}

    def test_get_categories(self, client):
        # Kategori oluşturma
        Category.objects.create(name="Test Category")

        # Kullanıcıyı giriş yapmış gibi ayarla
        client.login(username='testuser', password='testpass')

        # GET isteği gönderme
        response = client.get(reverse('category'))

        # İsteğin başarılı olup olmadığını kontrol etme
        assert response.status_code == 200
        assert len(response.data['data']) == 1
        assert response.data['data'][0]['name'] == "Test Category"

    def test_create_category(self, client):
        # Admin kullanıcıyı giriş yapmış gibi ayarla
        client.login(username='admin', password='adminpass')

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