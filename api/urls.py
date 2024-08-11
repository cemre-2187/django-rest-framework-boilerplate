from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from api.account.views import RegisterView,LoginView


urlpatterns = [
  path("register/", RegisterView.as_view(), name="register"),
  path("login/",LoginView.as_view(),name="login")
]
