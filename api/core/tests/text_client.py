import pytest
from django.test import TestCase
from rest_framework.test import APIClient


# @pytest.mark.usefixtures("test_user", "test_category", "test_blog", "admin_user", "get_access_token")
@pytest.mark.usefixtures("testfix")
class BaseTestClient:
    @pytest.fixture(autouse=True)
    def setup(self, testfix):
        self.testfix=testfix
        
    def tearDown(self):
        # Her testten sonra temiz bir ortam sağlamak için kullanılır.
        pass
