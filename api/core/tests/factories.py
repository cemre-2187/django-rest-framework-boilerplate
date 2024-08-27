import factory
from django.contrib.auth.models import User
from api.blog.models import Blog, Category
from faker import Faker

faker = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True 

    username = factory.LazyAttribute(lambda x: faker.user_name())
    password = factory.PostGenerationMethodCall('set_password', 'defaultpassword')  # Default password
    @factory.post_generation
    def set_password_hook(self, create, extracted, **kwargs):
        if create:
            self.save()

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.LazyAttribute(lambda x: faker.word())

class BlogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Blog

    title = factory.LazyAttribute(lambda x: faker.sentence())
    content = factory.LazyAttribute(lambda x: faker.text())
    author = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)