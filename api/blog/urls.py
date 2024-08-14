from django.urls import path
from .views import BlogView, CategoryView

urlpatterns = [
    path('', BlogView.as_view(), name='blog'),
    path('category/', CategoryView.as_view(), name='category'),
]

