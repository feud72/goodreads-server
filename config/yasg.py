from django.urls import path, include
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from drf_yasg import openapi

schema_url_v1_patterns = [
    path("api/v1/books/", include("books.urls")),
    path("api/v1/users/", include("users.urls")),
    path("api/v1/shelves/", include("shelves.urls")),
    path("api/v1/accounts/", include("accounts.urls")),
    path("api/v1/reviews/", include("reviews.urls")),
    path("api/v1/keywords/", include("keywords.urls")),
]

schema_view_v1 = get_schema_view(
    openapi.Info(
        title="Goodreads 클론 API",
        default_version="v1",
        description="""노마드코더 Goodreads 클론 해커톤 프로젝트, 톰리들 & SH Kim

아래 기술은 API 명세에 대한 간략한 설명(인자, 쿼리 파라미터, 응답 등)을 제공합니다.
실제 기능은 하단의 swagger의 Try it out을 작동시켜 확인할 수 있습니다.

---

### [API Link](https://github.com/feud72/goodreads-server/blob/master/api.md)

""",
    ),
    validators=["flex"],
    public=True,
    permission_classes=(AllowAny,),
    patterns=schema_url_v1_patterns,
)
