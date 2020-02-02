from django.urls import path
from . import views

app_name = "authentications"

urlpatterns = [
    path("register", views.registrationView, name="register"),
    path("login", views.loginView, name="login"),
]
