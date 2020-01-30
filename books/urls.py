from rest_framework.routers import DefaultRouter

from . import views


app_name = "books"
router = DefaultRouter()
router.register("", views.BookViewSet)

urlpatterns = router.urls
