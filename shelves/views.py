from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import viewsets

from .serializers import MyBookSerializer, MemoSerializer
from .models import MyBook, Memo


class BookShelfViewSet(viewsets.ModelViewSet):
    """
    책장 뷰셋

    ---
    """

    queryset = MyBook.objects.all()
    serializer_class = MyBookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.filter(owner__username=self.request.user).order_by(
            "-created_at"
        )
        return queryset

    def list(self, request, *args, **kwargs):
        """
책장의 책 리스트

## Specification
- **Method** :  GET
- **URL** : /api/v1/shelves/
- **Content-Type** : application/json; charset=utf-8
- **Parameters**

| 필드명 | 타입 | 필수여부 | 설명 |
| ---- | ---- | -------- | ----------- |
        """
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
My 책 생성

## Specification
- **Method** :  POST
- **URL** : /api/v1/shelves/
- **Content-Type** : application/json; charset=utf-8
- **Parameters**

| 필드명 | 타입 | 필수여부 | 설명 |
| ---- | ---- | -------- | ----------- |
| owner | string |   필수    | username (email)
| isbn | string |   필수    | isbn (13 length integer)
        """
        isbn = request.data["isbn"]
        username = request.user
        serializer = self.get_serializer(data={"username": username, "isbn": isbn})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        instance = MyBook.objects.get(owner__username=username, book__pk=isbn)
        serializer = self.get_serializer(instance)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @action(detail=True, methods=["get", "post", "put", "delete"])
    def memo(self, request, pk, *args, **kwargs):
        queryset = Memo.objects.filter(book__owner__username=request.user)
        serializer = MemoSerializer
        if request.method == "GET":
            data = serializer(queryset, many=True)
            return Response(status=status.HTTP_200_OK, data=data.data)
        if request.method == "POST":
            data = serializer(data={"book": pk, **request.data.dict()})
            if data.is_valid():
                data.save()
                message = {"message": "success"}
                return Response(status=status.HTTP_200_OK, data={"message": message})
            else:
                message = data.errors
                return Response(status=status.HTTP_200_OK, data={"message": message})
        else:
            return Response(status=status.HTTP_200_OK, data={"message": "OK"})
