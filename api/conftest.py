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
    
@pytest.fixture
def blog_data(test_user, test_category):
    return {
        'title': 'Create Test Blog',
        'content': 'This is a test blog content.',
        'author': test_user.id,
        'category': test_category.name
    }

@pytest.fixture
def category_data():
    return {
        'name':'New Category 2'
    }
    
@pytest.fixture
def get_access_token(client):
    url = '/account/login/'
    response = client.post(url, {'username': 'testuser', 'password': 'testpass'})
    assert response.status_code == 200
    print(response.data)
    return response.data['data']['access']

@pytest.fixture
def get_admin_access_token(client):
    url = '/account/login/'
    response = client.post(url, {'username': 'admin', 'password': 'adminpass'})
    print(response.data,"admin response")
    assert response.status_code == 200
    return response.data['data']['access']
