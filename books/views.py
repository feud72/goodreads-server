from rest_framework.viewsets import ModelViewSet
from .models import Book
from .serializers import BookSerializer


class BookViewSet(ModelViewSet):

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = "isbn"

    def get_queryset(self):
        term = self.request.query_params.get("term", None)
        year = self.request.query_params.get("year", None)
        author = self.request.query_params.get("author", None)
        query_dic = {"name": term, "pub_year": year, "author": author}

        filter_kwargs = {}
        for k, v in query_dic.items():
            if v is not None:
                filter_kwargs["{}__icontains".format(k)] = v
        try:
            books = Book.objects.filter(**filter_kwargs)
        except ValueError:
            books = Book.objects.all()
        return books
