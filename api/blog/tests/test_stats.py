import pytest
from django.urls import reverse
from django.contrib.auth.models import User

@pytest.mark.django_db
class TestStatsAPI:

    @pytest.fixture(scope='class')
    def setup_class(self, db):
        # Test için gerekli kullanıcıyı oluşturma
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_get_stats(self, client):
        # Kullanıcıyı giriş yapmış gibi ayarla
        client.login(username='testuser', password='testpass')

        # GET isteği gönderme
        response = client.get(reverse('stats'))

        # İsteğin başarılı olup olmadığını kontrol etme
        assert response.status_code == 200
        assert 'data' in response.data
        assert response.data['message'] == "Stats fetched successfully"