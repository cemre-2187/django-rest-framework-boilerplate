import pytest
from django.contrib.auth.models import User
from faker import Faker
from api.core.tests.factories import UserFactory, CategoryFactory, BlogFactory

faker = Faker()

@pytest.fixture
def test_user(db):
    return UserFactory(username='testuser', password='testpass')

@pytest.fixture
def admin_user(db):
    return UserFactory(username='admin', password='adminpass', is_staff=True, is_superuser=True)

@pytest.fixture
def test_category(db):
    return CategoryFactory(name="Test Category")

@pytest.fixture
def test_blog(test_user, test_category):
    return BlogFactory(author=test_user, category=test_category)

@pytest.fixture
def blog_data(test_user, test_category):
    return {
        'title': faker.sentence(),
        'content': faker.text(),
        'author': test_user.id,
        'category': test_category.name
    }

@pytest.fixture
def category_data():
    return {
        'name': faker.word()
    }
    
@pytest.fixture
def get_access_token(client):
    url = '/account/login/'
    response = client.post(url, {'username': 'testuser', 'password': 'testpass'})
    assert response.status_code == 200
    return response.data['data']['access']

@pytest.fixture
def get_admin_access_token(client):
    url = '/account/login/'
    response = client.post(url, {'username': 'admin', 'password': 'adminpass'})
    assert response.status_code == 200
    return response.data['data']['access']
