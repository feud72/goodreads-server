from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer


class BookViewSet(ModelViewSet):

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = "isbn"

    def list(self, request, *args, **kwargs):
        """
        GET api/v1/books/
        
        책의 목록을 반환.

        ---
        ### 파라미터
        - term    해당 단어가 포함된 책의 목록을 반환한다.

        - year    해당 년도에 출판된 책의 목록을 반환한다.

        - author  해당 저자가 포함된 책의 목록을 반환한다.

        """

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
        queryset = books
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

