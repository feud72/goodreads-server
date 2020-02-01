from django.urls import path, include
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from drf_yasg import openapi

schema_url_v1_patterns = [
    path("api/v1/books/", include("books.urls")),
    path("api/v1/users/", include("users.urls")),
]

schema_view_v1 = get_schema_view(
    openapi.Info(
        title="Goodreads 클론 API",
        default_version="v1",
        description="노마드코더 Goodreads 클론 해커톤 프로젝트, 톰리들 & SH Kim",
        contact=openapi.Contact(email="feud72@google.com"),
        license=openapi.License(name="MIT License"),
    ),
    validators=["flex"],
    public=True,
    permission_classes=(AllowAny,),
    patterns=schema_url_v1_patterns,
)
