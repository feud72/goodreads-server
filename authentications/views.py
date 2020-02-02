import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import RegistrationSerializer


@api_view(["POST"])
def loginView(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if not username or not password:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if user is not None:
        encoded_jwt = jwt.encode(
            {"id": user.pk}, settings.SECRET_KEY, algorithm="HS256"
        )
        return Response(data={"token": encoded_jwt})
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(["POST"])
def registrationView(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        user = serializer.save()
        data["response"] = "successfully registered a new user."
        data["email"] = user.email
        data["username"] = user.username
    else:
        data = serializer.errors
    return Response(data)
