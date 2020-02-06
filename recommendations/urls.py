from django.urls import path

from . import views

app_name = "recommendations"

urlpatterns = [
    path("detail/", views.detailView, name="detail"),
    path("recommend/", views.recommendView, name="recommend"),
    path("keyword/", views.keywordView, name="keyword"),
    path("popular/", views.popularView, name="popular"),
]
