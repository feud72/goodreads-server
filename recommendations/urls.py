from django.urls import path

from . import views

app_name = "recommendations"

urlpatterns = [
    path("popular/", views.popularView, name="popular"),
]
