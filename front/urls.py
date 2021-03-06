from django.urls import path
from . import views

app_name = "front"

urlpatterns = [
    path("", views.homeView, name="home"),
    path("popular/", views.popularView, name="popular"),
    path("popular/<str:sort>/", views.popularView, name="popular"),
    path("popular/<str:sort>/<int:page>/", views.popularView, name="popular"),
    path("keyword/<str:keyword>/", views.keywordView, name="keyword"),
    path("search/", views.searchView, name="search"),
    path("shelf/", views.shelfView, name="shelf"),
    path("shelf/<int:page>/", views.shelfView, name="shelf"),
    path("shelf/<int:id>/", views.shelfDetailView, name="shelf-detail"),
    path("review/", views.reviewView, name="review"),
    path("subscribe/", views.subscribeView, name="subscribe"),
    path("login/", views.loginView, name="login"),
    path("login/kakao/", views.kakaoLoginView, name="kakao"),
    path("login/kakao/callback/", views.kakaoCallbackView, name="kakaocallback"),
    path("signup/", views.signupView, name="signup"),
    path("logout/", views.logoutView, name="logout"),
    path("detail/<str:isbn>/", views.detailView, name="detail"),
    path("me/", views.meView, name="me"),
    path("me/edit/", views.meUpdateView, name="me-edit"),
]
