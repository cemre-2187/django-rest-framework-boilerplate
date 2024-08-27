import pytest
from django.test import TestCase
from rest_framework.test import APIClient



@pytest.mark.usefixtures("test_user", "test_category","category_data", "test_blog","blog_data", "admin_user", "get_access_token","get_admin_access_token")
class BaseTestClient:
    @pytest.fixture(autouse=True)
    def setup(self, test_user, test_category,category_data, test_blog,blog_data, admin_user, get_access_token, get_admin_access_token):

        self.test_user = test_user
        self.test_category = test_category
        self.category_data = category_data
        self.test_blog = test_blog
        self.blog_data = blog_data
        self.admin_user = admin_user
        self.get_access_token = get_access_token
        self.get_admin_access_token = get_admin_access_token
        self.client = APIClient()
        
        
    
    def tearDown(self):
        self.client.logout()
        pass
