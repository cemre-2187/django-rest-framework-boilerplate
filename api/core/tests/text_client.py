import pytest
from django.test import TestCase
from rest_framework.test import APIClient



@pytest.mark.usefixtures("test_user", "test_category", "test_blog", "admin_user", "get_access_token")
class BaseTestClient:
    @pytest.fixture(autouse=True)
    def setup(self, test_user, test_category, test_blog, admin_user, get_access_token):

        self.test_user = test_user
        self.test_category = test_category
        self.test_blog = test_blog
        self.admin_user = admin_user
        self.get_access_token = get_access_token
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + get_access_token)
        
    
        
    def tearDown(self):
        # Her testten sonra temiz bir ortam sağlamak için kullanılır.
        pass
