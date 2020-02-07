from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from utils.get_data import getPopular


@api_view(["GET"])
def popularView(request):
    if request.method == "GET":
        data = getPopular()
        return Response(status=status.HTTP_200_OK, data=data)
