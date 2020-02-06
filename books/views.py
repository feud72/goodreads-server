from rest_framework import filters, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Book
from .serializers import BookSerializer

from utils.get_data import getDetail


class BookViewSet(ModelViewSet):
    """
    Book View Set Doc
    ---
    list:
      omit_serializer: false
      parameters:
          - name: search
            type: string
    """

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "pub_year", "author"]
    ordering_fields = ["name", "author", "pub_year"]

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = "isbn"
    http_method_names = [u"get"]

    def retrieve(self, request, *args, **kwargs):
        isbn = self.kwargs["isbn"]
        if isbn is not None:
            try:
                data = getDetail(isbn)
                return Response(status=status.HTTP_200_OK, data=data)
            except Exception:
                pass
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
