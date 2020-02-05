from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import viewsets

from .serializers import BookShelfSerializer, MyBookSerializer, MemoSerializer
from .models import BookShelf, MyBook, Memo


class BookShelfViewSet(viewsets.ModelViewSet):
    """
    BookShelfViewSet

    ---
    """

    queryset = BookShelf.objects.all()
    serializer_class = BookShelfSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return BookShelf.objects.all()

    def list(self, request, *args, **kwargs):
        permission = self.get_permissions()
        queryset = self.get_queryset()
        if permission is IsAuthenticated:
            queryset = self.request.user.bookshelf_set.all()
        else:
            owner = self.request.query_params.get("owner", None)
            queryset = self.get_queryset().filter(owner__pk=owner)
        serializer = self.get_serializer(queryset, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def create(self, request, *args, **kwargs):
        """
        POST: 책장을 만든다.

        ---
        key

        owner   |   필수    | pk 값 (id)
        name    |   옵션    | 책장의 이름. 기본값은 My Bookshelf
        gender  |   옵션    | 성별. M(남성), F(여성), N(제공하지 않음), 기본값은 N
        age     |   옵션    | 나이. integer

        ---
        id, created_at, name,
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
