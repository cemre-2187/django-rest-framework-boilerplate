import pytest
from django.test import TestCase
from rest_framework.test import APIClient


# @pytest.mark.usefixtures("test_user", "test_category", "test_blog", "admin_user", "get_access_token")
class BaseTestClient(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # self.test_user = getattr(self, 'test_user', None)
        # self.test_category = test_category
        # print(self.test_category )
        # self.test_blog = getattr(self, 'test_blog', None)
        # self.admin_user = getattr(self, 'admin_user', None)
        # self.access_token = getattr(self, 'get_access_token', None)
        # self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        
    def tearDown(self):
        # Her testten sonra temiz bir ortam sağlamak için kullanılır.
        pass
