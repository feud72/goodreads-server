from django.urls import path
from . import views

app_name = "front"

urlpatterns = [
    path("", views.homeView, name="home"),
    path("popular/", views.popularView, name="popular"),
    path("recent/", views.recentView, name="recent"),
    path("login/", views.loginView, name="login"),
    path("logout/", views.logoutView, name="logout"),
    path("detail/<str:isbn>/", views.detailView, name="detail"),
]
