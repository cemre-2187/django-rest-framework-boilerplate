import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from api.blog.models import Blog, Category
from rest_framework.test import APIClient
from api.core.tests.text_client import BaseTestClient
from django.test import TestCase


@pytest.mark.django_db
class TestBlogAPI(BaseTestClient):
  
    def test_get_blogs(self):
        
        # Login For Test User
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.get_access_token)
        
        # Test bloğunu oluşturma
        Blog.objects.create(title="Test Blog", content="This is a test blog content.", author=self.test_user, category=self.test_category)

        # GET isteği gönderme
        response = self.client.get(reverse('blog'))

        # # İsteğin başarılı olup olmadığını kontrol etme
        assert response.status_code == 200
        assert len(response.data['data']) == 2
        assert response.data['data'][0]['title'] == "Test Blog"

    def test_create_blog(self):
        # Login For  User
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.get_access_token)
        
        # POST isteği gönderme
        response = self.client.post(reverse('blog'), self.blog_data)

        # Blogun başarılı bir şekilde oluşturulup oluşturulmadığını kontrol etme
        assert response.status_code == 200
        assert Blog.objects.count() == 2
        # get blog with title filter
        assert Blog.objects.filter(title="Create Test Blog").exists()

    def test_create_blog_unauthorized(self):
        # Giriş yapmadan POST isteği gönderme
        response = self.client.post(reverse('blog'), self.blog_data)

        # Blog oluşturma isteğinin yetkisiz olup olmadığını kontrol etme
        assert response.status_code == 401
        assert Blog.objects.count() == 1

    def test_create_blog_invalid_author(self, client, test_user, blog_data):
        # Login For  User
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.get_access_token)

        # Farklı bir yazar ile blog oluşturma denemesi
        blog_data['author'] = test_user.id + 1
        response = client.post(reverse('blog'), blog_data)

        # Blog oluşturma isteğinin yetkisiz olup olmadığını kontrol etme
        assert response.status_code == 401
        assert Blog.objects.count() == 1