import pytest
from django.test import TestCase
from rest_framework.test import APIClient


@pytest.mark.usefixtures("test_user", "test_category", "test_blog", "admin_user", "get_access_token")
class BaseTestClient(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.test_user = self._get_fixture('test_user')
        self.test_category = self._get_fixture('test_category')
        self.test_blog = self._get_fixture('test_blog')
        self.admin_user = self._get_fixture('admin_user')
        self.access_token = self._get_fixture('get_access_token')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        
    def tearDown(self):
        # Her testten sonra temiz bir ortam sağlamak için kullanılır.
        pass
