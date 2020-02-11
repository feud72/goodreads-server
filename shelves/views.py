from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
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
| owner | string |   필수    | user pk (id)
| book | string |   필수    | book pk (isbn)

        """
        isbn = request.data["isbn"]
        username = request.user
        serializer = self.get_serializer(data={"username": username, "isbn": isbn})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        instance = MyBook.objects.get(book__pk=isbn)
        serializer = self.get_serializer(instance)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    # return Response(
    #            status=status.HTTP_401_UNAUTHORIZED, data={"error": "Anauthorized."}
    #       )


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def myBookView(request):
    queryset = MyBook.objects.filter(bookshelf__owner__username=request.user)
    serializer = MyBookSerializer

    if request.method == "GET":
        data = serializer(queryset, many=True)
        return Response(status=status.HTTP_200_OK, data=data.data)
    if request.method == "POST":
        pass


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def memoView(request):
    queryset = Memo.objects.filter(book__bookshelf__owner__username=request.user)
    serializer = MemoSerializer

    if request.method == "GET":
        data = serializer(queryset, many=True)
        return Response(status=status.HTTP_200_OK, data=data.data)
    if request.method == "POST":
        pass
