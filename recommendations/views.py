from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from utils.get_data import popular


@api_view(["GET"])
def popularView(request):
    # serializer = MyBookSerializer
    if request.method == "GET":
        data = popular()
        return Response(status=status.HTTP_200_OK, data=data)
