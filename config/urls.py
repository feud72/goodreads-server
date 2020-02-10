"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static

from .yasg import schema_view_v1

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/books/", include("books.urls")),
    path("api/v1/users/", include("users.urls")),
    path("api/v1/accounts/", include("accounts.urls")),
    path("api/v1/shelves/", include("shelves.urls")),
    path("api/v1/recommendations/", include("recommendations.urls")),
    path("", include("front.urls")),
]

urlpatterns += [
    re_path(
        r"^api/v1/swagger(?P<format>\.json|\.yaml)/$",
        schema_view_v1.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^api/v1/swagger/$",
        schema_view_v1.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^api/v1/doc/$",
        schema_view_v1.with_ui("redoc", cache_timeout=0),
        name="schema-redoc-v1",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
