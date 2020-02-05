from django.urls import path

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"bookshelf", views.BookShelfViewSet, basename="bookshelf")

urlpatterns = router.urls

urlpatterns += [
    path("mybook/", views.myBookView, name="mybook"),
    path("memo/", views.memoView, name="memo"),
]
