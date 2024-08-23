import pytest
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
def test_blog(test_user, test_category):
    return Blog.objects.create(
        title="Test Blog",
        content="This is a test blog content.",
        author=test_user,
        category=test_category
    )