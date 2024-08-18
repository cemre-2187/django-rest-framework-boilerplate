import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from api.blog.models import Blog, Category

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
    url = reverse('api.account:login')
    response = client.post(url, {'username': 'testuser', 'password': 'testpass'})
    assert response.status_code == 200
    return response.data['access']

@pytest.mark.django_db
class TestBlogAPI:

    def test_get_blogs(self, client, test_user, test_category,get_access_token):
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + get_access_token)
        # Test bloğunu oluşturma
        Blog.objects.create(title="Test Blog", content="This is a test blog content.", author=test_user, category=test_category)

        # Kullanıcıyı giriş yapmış gibi ayarla
        client.login(username='testuser', password='testpass')

        # GET isteği gönderme
        response = client.get(reverse('blog'))

        # İsteğin başarılı olup olmadığını kontrol etme
        assert response.status_code == 200
        assert len(response.data['data']) == 1
        assert response.data['data'][0]['title'] == "Test Blog"

    def test_create_blog(self, client, test_user, blog_data, get_access_token):
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + get_access_token)
        # Kullanıcıyı giriş yapmış gibi ayarla
        client.login(username='testuser', password='testpass')

        # POST isteği gönderme
        response = client.post(reverse('blog'), blog_data)

        # Blogun başarılı bir şekilde oluşturulup oluşturulmadığını kontrol etme
        assert response.status_code == 200
        assert Blog.objects.count() == 1
        assert Blog.objects.get().title == "Test Blog"

    def test_create_blog_unauthorized(self, client, blog_data):
        # Giriş yapmadan POST isteği gönderme
        response = client.post(reverse('blog'), blog_data)

        # Blog oluşturma isteğinin yetkisiz olup olmadığını kontrol etme
        assert response.status_code == 401
        assert Blog.objects.count() == 0

    def test_create_blog_invalid_author(self, client, test_user, blog_data):
        # Kullanıcıyı giriş yapmış gibi ayarla
        client.login(username='testuser', password='testpass')

        # Farklı bir yazar ile blog oluşturma denemesi
        blog_data['author'] = test_user.id + 1
        response = client.post(reverse('blog'), blog_data)

        # Blog oluşturma isteğinin yetkisiz olup olmadığını kontrol etme
        assert response.status_code == 401
        assert Blog.objects.count() == 0