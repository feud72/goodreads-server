from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import viewsets

from .serializers import MyBookSerializer
from .models import MyBook


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
        queryset = queryset.filter(owner__username=self.request.user)
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
| isbn | string |   필수    | isbn (13 length)
        """
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
