import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from api.blog.models import Blog, Category
from rest_framework.test import APIClient
from api.core.tests.text_client import BaseTestClient


@pytest.mark.django_db
class TestBlogAPI(BaseTestClient):
  
    def test_get_blogs(self):
        
        # Login for the test user
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.get_access_token)
        
        # Create a test blog
        Blog.objects.create(title="Test Blog", content="This is a test blog content.", author=self.test_user, category=self.test_category)

        # Send a GET request
        response = self.client.get(reverse('blog'))

        # Check if the request was successful
        assert response.status_code == 200
        assert len(response.data['data']) == 2
        assert response.data['data'][0]['title'] == "Test Blog"

    def test_create_blog(self):
        # Login for the user
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.get_access_token)
        
        # Send a POST request
        response = self.client.post(reverse('blog'), self.blog_data)

        # Check if the blog was created successfully
        assert response.status_code == 200
        assert Blog.objects.count() == 2
        # Get blog with title filter
        assert Blog.objects.filter(title="Create Test Blog").exists()

    def test_create_blog_unauthorized(self):
        # Send a POST request without logging in
        response = self.client.post(reverse('blog'), self.blog_data)

        # Check if the blog creation request was unauthorized
        assert response.status_code == 401
        assert Blog.objects.count() == 1

    def test_create_blog_invalid_author(self, client, test_user, blog_data):
        # Login for the user
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.get_access_token)

        # Attempt to create a blog with a different author
        blog_data['author'] = test_user.id + 1
        response = client.post(reverse('blog'), blog_data)

        # Check if the blog creation request was unauthorized
        assert response.status_code == 401
        assert Blog.objects.count() == 1