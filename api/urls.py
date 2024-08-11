from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from api.account.views import RegisterView


urlpatterns = [
  path("register/", RegisterView.as_view(), name="register"),
]
