import pytest
from django.test import TestCase
from rest_framework.test import APIClient


@pytest.mark.usefixtures("test_user", "test_category", "test_blog", "admin_user", "get_access_token")
class BaseTestClient(TestCase):
    def setUp(self):
        self.client = APIClient()
        # self.test_user, self.test_category, self.test_blog gibi özelliklere
        # `self` üzerinden erişmek isterseniz, setUp'da elle atayabilirsiniz.

    def tearDown(self):
        # Her testten sonra temiz bir ortam sağlamak için kullanılır.
        pass
