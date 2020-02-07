from rest_framework import filters, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from .models import Book
from .serializers import BookSerializer

from utils.get_data import (
    getDetail,
    getRecommendByISBN,
    getKeywordList,
    kakaoSearch,
    getPopular,
)


class BookViewSet(ModelViewSet):
    """
    책
    """

    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "pub_year", "author"]

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = "isbn"
    http_method_names = [u"get", u"post"]

    def list(self, request, *args, **kwargs):
        """
책의 전체 리스트, search 쿼리로 부분적인 검색 결과를 얻을 수 있다.

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
Create a book.

## Specification
- **Parameters**

| 필드명 | 타입 | 필수여부 | 설명 |
| ---- | ---- | -------- | ----------- |
| isbn | string | Required | ISBN 13자리를 입력한다.|
        """
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
책의 상세 정보

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
        if isbn is not None:
            try:
                data = getDetail(isbn)
                return Response(status=status.HTTP_200_OK, data=data)
            except Exception:
                pass
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["GET"])
    def recommend(self, request, isbn, *args, **kwargs):
        data = getRecommendByISBN(isbn=isbn)
        return Response(status=status.HTTP_200_OK, data=data)

    @action(detail=True, methods=["GET"])
    def keyword(self, request, isbn, *args, **kwargs):
        data = getKeywordList(isbn=isbn)
        return Response(status=status.HTTP_200_OK, data=data)

    @action(detail=False, methods=["GET"])
    def search(self, request, *args, **kwargs):
        query = self.request.query_params["search"]
        data = kakaoSearch(query)
        return Response(status=status.HTTP_200_OK, data=data)

    @action(
        detail=False, url_path="recommend", methods=["GET"],
    )
    def recommendByUserInfo(self, request, *args, **kwargs):
        data = getPopular()
        return Response(status=status.HTTP_200_OK, data=data)
