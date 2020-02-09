from django.urls import path
from . import views

app_name = "front"

urlpatterns = [
    path("", views.homeView, name="home"),
    path("<str:isbn>/", views.detailView, name="detail"),
    path("login", views.loginView, name="login"),
    path("signup", views.signupView, name="signup"),
]
