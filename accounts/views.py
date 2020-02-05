from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegistrationSerializer

from shelves.serializers import BookShelfSerializer
from utils.jwt import encode_jwt


class LoginView(APIView):
    """
    Validate username and password.

    ---
    username|string|required
    password|string|required
    """

    def post(self, request):
        username = request.data.get("email", None)
        password = request.data.get("password", None)
        if not username:
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data={"error": "Email is required."}
            )
        elif not password:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": "Password is required."},
            )
        user = authenticate(username=username, password=password)
        print(username, password)
        if user is not None:
            encoded_jwt = encode_jwt("pk", user.pk)
            return Response(
                status=status.HTTP_200_OK,
                data={"message": "success", "token": encoded_jwt, "id": user.pk},
            )
        else:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED, data={"error": "Unauthorized."}
            )


class SignupView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        message = {}
        if serializer.is_valid():
            user = serializer.save()
            message["message"] = "success"
            message["email"] = user.email
            message["current_bookshelf"] = BookShelfSerializer(
                user.current_bookshelf
            ).data
            return Response(status=status.HTTP_201_CREATED, data=message)
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data={"error": serializer.errors}
            )
