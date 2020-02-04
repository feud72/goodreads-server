from django.urls import path

from . import views, social_login

app_name = "accounts"

urlpatterns = [
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("login/kakao/", social_login.kakao_login, name="kakao-login"),
    path("login/kakao/callback", social_login.kakao_callback, name="kakao-callback"),
]
