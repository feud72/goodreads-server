from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from utils.get_data import getPopular, getDetail, getKeywordList, getRecommend


@api_view(["GET"])
def popularView(request):
    """
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "pub_year", "author"]
    ordering_fields = ["name", "author", "pub_year"]
    """

    # serializer = MyBookSerializer
    if request.method == "GET":
        data = getPopular()
        return Response(status=status.HTTP_200_OK, data=data)


@api_view(["GET"])
def recommendView(request):
    if request.method == "GET":
        data = getRecommend()
        return Response(status=status.HTTP_200_OK, data=data)


@api_view(["GET"])
def keywordView(request):
    if request.method == "GET":
        data = getKeywordList()
        return Response(status=status.HTTP_200_OK, data=data)


@api_view(["GET"])
def detailView(request):
    if request.method == "GET":
        data = getDetail()
        return Response(status=status.HTTP_200_OK, data=data)
