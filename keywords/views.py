from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Keyword
from .serializers import KeywordSerializer, RelatedBookSerializer


class KeywordViewSet(ModelViewSet):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer
    lookup_field = "word"
    http_method_names = [u"get"]

    def retrieve(self, request, *args, **kwargs):
        word = self.kwargs["word"]
        queryset = Keyword.objects.filter(word=word)
        serializer = RelatedBookSerializer(queryset, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
