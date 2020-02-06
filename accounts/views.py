from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from .serializers import RegistrationSerializer, LoginSerializer

from shelves.serializers import BookShelfSerializer
from utils.jwt import encode_jwt


class LoginView(GenericAPIView):
    """
    Login
    """

    serializer_class = LoginSerializer

    def post(self, request):
        """
        Login
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = get_user_model().objects.get(email=email)
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
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


#            username = request.data.get("email", None)
#            password = request.data.get("password", None)
#
#            if not username:
#                return Response(
#                    status=status.HTTP_400_BAD_REQUEST,
#                    data={"error": "Email is required."},
#                )
#            elif not password:
#                return Response(
#                    status=status.HTTP_400_BAD_REQUEST,
#                    data={"error": "Password is required."},
#                )


class SignupView(GenericAPIView):
    """
    Signup
    ----
    """

    serializer_class = RegistrationSerializer

    def post(self, request):
        """
        Signup
        ---
        """
        serializer = self.get_serializer(data=request.data)
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
