from rest_framework.routers import DefaultRouter

from . import views

app_name = "keywords"
router = DefaultRouter()
router.register("", views.KeywordViewSet)

urlpatterns = router.urls
