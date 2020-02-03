import jwt

from django.conf import settings
from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegistrationSerializer


class LoginView(APIView):
    """
    Validate username and password.

    ---
    username|string|required
    password|string|required
    """

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user is not None:
            encoded_jwt = jwt.encode(
                {"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256"
            )
            return Response(data={"token": encoded_jwt, "id": user.pk})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class SignupView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data["message"] = "Successfully registered a new user."
            data["username"] = user.username
            data["email"] = user.email
        else:
            data = serializer.errors
        return Response(status=status.HTTP_201_CREATED, data=data)
