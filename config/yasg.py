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

## /accounts/
계정 관련 회원가입, 로그인 기능을 담당합니다.
인증 토큰을 요구하지 않습니다.

### GET

#### /accounts/kakao/
필수 인자 : 없음

### POST

#### /accounts/login/ : 로그인
필수 인자 : email, password
응답
 - 성공 : 200 {"message", "token", "id"}
 - 실패 : 400 {"detail"} 또는 {"non_field_errors"} (JSON 형태로 반환)

#### /accounts/signup/ : 회원가입
필수 인자 : email, password1, password2
응답
 - 성공 : 201 {"message", "email"}
 - 실패 : 400 {"detail"} 또는 {"non_field_errors"} (JSON 형태로 반환)

---

## /books/
책의 목록을 얻거나, 책의 ISBN을 입력하여 새로운 책을 만들 수 있습니다.
인증 토큰을 요구하지 않습니다.

### GET

#### /books/ : DB가 가지고 있는 책의 목록을 반환합니다. 현재 페이지네이션은 25개로 고정.
쿼리 파라미터
 - search : 검색어 (옵션)
 - page : 페이지 (옵션)

#### /books/recommend/ : 도서관 인기 대출 순위에서 랜덤하게 10개를 추출하여 보여줍니다.
쿼리 파라미터 : 없음
응답 : 리스트를 반환합니다. 각각의 원소들은 GET /books/{isbn}/과 형식이 같습니다.

#### /books/search/ : 카카오 API를 통해 책을 검색하여 보여줍니다.
(현재 버그로 search 쿼리 파라미터를 입력하지 않으면 server error 발생)
쿼리 파라미터
 - search : 검색어 (필수)
 - page : 페이지 (옵션)
응답
 - 성공 : 200 리스트를 반환합니다. 각각의 원소들은 GET /books/{isbn}/과 형식이 같습니다.

### POST

#### /books/ : 책을 생성합니다.
필수 인자 : isbn
응답
 - 성공 : 201 {"title", "author", "publisher", "pub_year", "isbn", "description", "bookImage"}
 - 실패 : 400 {"isbn"} (JSON 형태로 반환)

(작성중)

---

## /books/{isbn}/
책의 상세 정보를 얻을 수 있습니다.
인증 토큰을 요구하지 않습니다.

### GET

####/books/{isbn}/
#### /books/{isbn}/recommend/
#### /books/{isbn}/keyword/

---

## /shelves/

###GET

#### /shelves/
필요 조건
 - header parameter : {"Authorization": "Token xxxxxxxxxxxx"}

### POST

#### /sheves/

---

## /shelves/{id}/

### GET

#### /shelves/{id}/

### POST

#### /shelves/{id}/

###PUT, PATCH, DELETE

#### /shelves/{id}/

---

## /shelves/{id}/memo/

### GET

####/shelves/{id}/memo/

###POST

####/shelves/{id}/memo/

###PUT, DELETE

####/shelves/{id}/memo/

""",
        contact=openapi.Contact(email="feud72@google.com"),
        license=openapi.License(name="MIT License"),
    ),
    validators=["flex"],
    public=True,
    permission_classes=(AllowAny,),
    patterns=schema_url_v1_patterns,
)
