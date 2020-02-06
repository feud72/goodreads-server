from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import viewsets

from .serializers import BookShelfSerializer, MyBookSerializer, MemoSerializer
from .models import BookShelf, MyBook, Memo


class BookShelfViewSet(viewsets.ModelViewSet):
    """
    책장 뷰셋

    ---
    """

    queryset = BookShelf.objects.all()
    serializer_class = BookShelfSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return BookShelf.objects.all()

    def list(self, request, *args, **kwargs):
        """
책장의 전체 리스트

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
책장 생성

## Specification
- **Method** :  POST
- **URL** : /api/v1/shelves/
- **Content-Type** : application/json; charset=utf-8
- **Parameters**

| 필드명 | 타입 | 필수여부 | 설명 |
| ---- | ---- | -------- | ----------- |
| owner | string |   필수    | pk 값 (id)
| name | string |   옵션    | 책장의 이름. 기본값은 My Bookshelf
| gender | string|   옵션    | 성별. M(남성), F(여성), N(제공하지 않음), 기본값은 N
| age   | string |   옵션    | 나이. integer

        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        owner = serializer.validated_data["owner"]
        if request.user == owner:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        else:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED, data={"error": "Anauthorized."}
            )


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
