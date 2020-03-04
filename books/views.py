from django.db.models import Avg, Value
from django.db.models.functions import Coalesce

from rest_framework import filters, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

import django_rq

from .models import Book
from .serializers import BookSerializer
from .tasks import create_keywords

from utils.get_data import (
    getDetail,
    getRecommendByISBN,
    kakaoSearch,
)

from keywords.serializers import KeywordSerializer
from keywords.models import Keyword


class BookViewSet(ModelViewSet):
    """
    책
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = "isbn"
    http_method_names = [u"get", u"post"]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "pub_year", "author"]
    ordering_fields = "__all__"
    ordering = ["-avg_star", "-num_views"]

    def queue(self, isbn):
        django_rq.enqueue(create_keywords, isbn)

    def get_queryset(self):
        return Book.objects.annotate(avg_star=Coalesce(Avg("review__star"), Value(0)),)

    def list(self, request, *args, **kwargs):
        """
책의 전체 리스트

---
search 쿼리를 옵션 인자로 갖는다.
search 쿼리로 부분적인 검색 결과를 얻을 수 있다.

## Specification
- **Method** :  GET
- **URL** : /api/v1/books/
- **Content-Type** : application/json; charset=utf-8
- **Parameters**

| 필드명 | 타입 | 필수여부 | 설명 |
| ---- | ---- | -------- | ----------- |
| search | string | Option | 책의 이름, 출판년도, 저자를 입력한다.|
        """
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
책을 생성한다. isbn을 필수 인자로 갖는다.

---
isbn으로 국립중앙도서관 API에서 서지 정보를 불러와 내부 DB에 저장한다.

## Specification
- **Parameters**

| 필드명 | 타입 | 필수여부 | 설명 |
| ---- | ---- | -------- | ----------- |
| isbn | string | Required | ISBN 13자리를 입력한다.|
        """
        isbn = request.data.get("isbn")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        instance = Book.objects.get(isbn=isbn)
        serializer = self.get_serializer(instance)
        self.queue(isbn)
        return Response(
            data=serializer.data, status=status.HTTP_201_CREATED, headers=headers,
        )

    def retrieve(self, request, *args, **kwargs):
        """
책의 상세 정보를 출력한다.

---
isbn을 path의 인자로 가진다.

## Specification
- **Method** :  GET
- **URL** : /api/v1/books/{isbn}/
- **Content-Type** : application/json; charset=utf-8
- **Parameters**

| 필드명 | 타입 | 필수여부 | 설명 |
| ---- | ---- | -------- | ----------- |
| isbn | string | Required | (path) isbn 13자리를 입력합니다. |
        """
        isbn = self.kwargs["isbn"]
        if not Book.objects.filter(isbn=isbn).exists():
            data = getDetail(isbn)
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                self.perform_create(serializer)
            else:
                return Response(
                    data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
        self.queue(isbn)
        instance = self.get_object()
        current_ip = request.META.get("REMOTE_ADDR")
        if instance.last_ip != current_ip:
            instance.last_ip = current_ip
            instance.num_views += 1
            instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=["GET"])
    def recommend(self, request, isbn, *args, **kwargs):
        """
현재의 책과 관련된 추천 도서를 리스트로 출력한다.

---
isbn을 path의 인자로 가진다.

## Specification
- **Method** :  GET
- **URL** : /api/v1/books/{isbn}/recommend/
- **Content-Type** : application/json; charset=utf-8
- **Parameters**

| 필드명 | 타입 | 필수여부 | 설명 |
| ---- | ---- | -------- | ----------- |
| isbn | string | Required | (path) isbn 13자리를 입력합니다. |
        """
        data = getRecommendByISBN(isbn=isbn)
        return Response(status=status.HTTP_200_OK, data=data)

    @action(detail=True, methods=["GET"])
    def keywords(self, request, isbn, *args, **kwargs):
        """
현재의 책의 연관된 단어(word)와 가중치(weight)를 리스트로 출력한다.

---
isbn을 path의 인자로 가진다.

## Specification
- **Method** :  GET
- **URL** : /api/v1/books/{isbn}/keywords/
- **Content-Type** : application/json; charset=utf-8
- **Parameters**

| 필드명 | 타입 | 필수여부 | 설명 |
| ---- | ---- | -------- | ----------- |
| isbn | string | Required | (path) isbn 13자리를 입력합니다. |
        """
        queryset = Keyword.objects.filter(book__isbn=isbn)
        serializer = KeywordSerializer(queryset, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=False, methods=["GET"])
    def search(self, request, *args, **kwargs):
        """
카카오 책 검색 API를 사용하여 도서 리스트를 검색한다.

---
isbn, title, author, description을 가진 dictionary item의 list를 응답한다.

## Specification
- **Method** :  GET
- **URL** : /api/v1/books/{isbn}/recommend/
- **Content-Type** : application/json; charset=utf-8
- **Parameters**

| 필드명 | 타입 | 필수여부 | 설명 |
| ---- | ---- | -------- | ----------- |
| isbn | string | Required | (path) isbn 13자리를 입력합니다. |
        """
        query = self.request.query_params["search"]
        page = 1
        if "page" in self.request.query_params:
            page = self.request.query_params["page"]
        data = kakaoSearch(query, page)
        if data:
            return Response(status=status.HTTP_200_OK, data=data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data)
