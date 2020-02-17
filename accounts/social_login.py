from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import jwt
import requests


class KakaoException(Exception):
    pass


def kakao_get_profile(access_token):
    try:
        profile_request = requests.get(
            "https://kapi.kakao.com/v1/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        return profile_json
    except KakaoException:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(
    ["POST",]
)
def kakao(request):
    """
카카오와 해커톤 로그인 연동
    """
    try:
        access_token = request.data["token"]
        profile_json = kakao_get_profile(access_token)
        email = profile_json.get("kaccount_email", None)
        if email is None:
            raise KakaoException()
        properties = profile_json.get("properties")
        nickname = properties.get("nickname")
        user, created = get_user_model().objects.get_or_create(
            email=email, username=email, first_name=nickname, login_method="kakao",
        )
        if created:
            user.set_unusable_password()
            user.save()
            data = {}
            data["message"] = "Successfully registered a new user."
            data["username"] = user.username
            data["email"] = user.email
            return Response(status=status.HTTP_201_CREATED, data=data)
        else:
            if user.login_method == "kakao":
                encoded_jwt = jwt.encode(
                    {"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256"
                )
                return Response(data={"token": encoded_jwt, "id": user.pk})
            else:
                raise KakaoException()
    except KakaoException:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
