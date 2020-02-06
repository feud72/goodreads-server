from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from drf_yasg.utils import swagger_auto_schema

from drf_yasg import openapi

from .models import Book
from .serializers import BookSerializer


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

    filter_backends = [SearchFilter]
    search_fields = ["name", "pub_year", "author"]

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = "isbn"
    pagination_class = PageNumberPagination
    page_size = 10
    http_method_names = [u"get"]
    param = openapi.Parameter(
        "search",
        openapi.IN_QUERY,
        description="Search~~ blahblah",
        type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(manual_parameters=[param],)
    def list(self, request, *args, **kwargs):
        """
        책의 목록을 반환.
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)


#    def retrieve(self, request, *args, **kwargs):
#        """
#        Show Detail with ISBN13 code
#        """
#        instance = self.get_object()
#        serializer = self.get_serializer(instance)
#        return Response(serializer.data)
