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
        Create Bookshelf
        """
        super.create()


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
