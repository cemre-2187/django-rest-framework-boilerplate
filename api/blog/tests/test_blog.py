import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from api.blog.models import Blog, Category
from rest_framework.test import APIClient
from api.core.tests.text_client import BaseTestClient
from django.test import TestCase

@pytest.mark.django_db
class TestBlogAPI(TestCase):
    # @pytest.mark.usefixtures("test_user", "test_category", "test_blog", "admin_user", "get_access_token")
    def test_get_blogs(testfix):
        print(testfix)
        assert type(testfix)==str
        # client=APIClient()
        # client.credentials(HTTP_AUTHORIZATION='Bearer ' + get_access_token)
        
        # Test bloğunu oluşturma
        # Blog.objects.create(title="Test Blog", content="This is a test blog content.", author=self.test_user, category=test_category)

        # GET isteği gönderme
        # response = client.get(reverse('blog'))

        # # İsteğin başarılı olup olmadığını kontrol etme
        # assert response.status_code == 200
        # assert len(response.data['data']) == 1
        # assert response.data['data'][0]['title'] == "Test Blog"

    # def test_create_blog(self, client, test_user, blog_data, get_access_token):
    #     client=APIClient()
    #     client.credentials(HTTP_AUTHORIZATION='Bearer ' + get_access_token)
        
    #     # POST isteği gönderme
    #     response = client.post(reverse('blog'), blog_data)

    #     # Blogun başarılı bir şekilde oluşturulup oluşturulmadığını kontrol etme
    #     assert response.status_code == 200
    #     assert Blog.objects.count() == 1
    #     assert Blog.objects.get().title == "Test Blog"

    # def test_create_blog_unauthorized(self, client, blog_data):
    #     # Giriş yapmadan POST isteği gönderme
    #     response = client.post(reverse('blog'), blog_data)

    #     # Blog oluşturma isteğinin yetkisiz olup olmadığını kontrol etme
    #     assert response.status_code == 401
    #     assert Blog.objects.count() == 0

    # def test_create_blog_invalid_author(self, client, test_user, blog_data):
    #     # Kullanıcıyı giriş yapmış gibi ayarla
    #     client.login(username='testuser', password='testpass')

    #     # Farklı bir yazar ile blog oluşturma denemesi
    #     blog_data['author'] = test_user.id + 1
    #     response = client.post(reverse('blog'), blog_data)

    #     # Blog oluşturma isteğinin yetkisiz olup olmadığını kontrol etme
    #     assert response.status_code == 401
    #     assert Blog.objects.count() == 0