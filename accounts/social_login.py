from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import jwt
import requests

from utils.username import get_random_name


class KakaoException(Exception):
    pass


def kakao_get_profile(access_token):
    try:
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        return profile_json
    except KakaoException:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(
    ["POST",]
)
def kakaoUnlink(request):
    try:
        access_token = request.data["token"]
        url = "https://kapi.kakao.com/v1/user/unlink"
        headers = {"Authorization": f"Bearer {access_token}"}
        req = requests.post(url, headers=headers)
        message = req.json()
        return Response(data=message)
    except KakaoException:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(
    ["POST",]
)
def kakaoLogin(request):
    """
카카오와 해커톤 로그인 연동
    """
    try:
        access_token = request.data["token"]
        profile_json = kakao_get_profile(access_token)
        email = profile_json["kakao_account"]["email"]
        if email is None:
            url = "https://kapi.kakao.com/v1/user/unlink"
            headers = {"Authorization": f"Bearer {access_token}"}
            data = requests.post(url, headers=headers)
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data.json())
        else:
            if get_user_model().objects.filter(username=email).exists():
                user = get_user_model().objects.get(
                    username=email, login_method="kakao",
                )
                if user.login_method == "kakao":
                    encoded_jwt = jwt.encode(
                        {"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256"
                    )
                    return Response(data={"token": encoded_jwt, "id": user.pk})
                else:
                    raise KakaoException()
            else:
                nickname = get_random_name()
                user = get_user_model().objects.create(
                    email=email,
                    username=email,
                    nickname=nickname,
                    login_method="kakao",
                )
                user.set_unusable_password()
                user.save()
                data = {}
                data["message"] = "Successfully registered a new user."
                data["username"] = user.username
                return Response(status=status.HTTP_201_CREATED, data=data)
    except KakaoException:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
