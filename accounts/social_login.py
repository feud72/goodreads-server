import os

from django.conf import settings
from django.shortcuts import redirect

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import jwt
import requests

from users.models import User


def kakao_login(request):
    """
    Kakao login
    """
    client_id = os.environ.get("KAKAO_ID")
    base_uri = os.environ.get("BASE_URI")
    redirect_uri = base_uri + "/api/v1/accounts/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )


class KakaoException(Exception):
    pass


def kakao_get_token(request):
    try:
        client_id = os.environ.get("KAKAO_ID")
        code = request.GET.get("code")
        base_uri = os.environ.get("BASE_URI")
        redirect_uri = base_uri + "/api/v1/accounts/login/kakao/callback"
        payload = f"grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        url = "https://kauth.kakao.com/oauth/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Cache-Control": "no-cache",
        }
        token_request = requests.post(url, data=payload, headers=headers)
        token_json = token_request.json()
        error = token_json.get("error", None)
        if error is not None:
            raise KakaoException()
        access_token = token_json.get("access_token")
        return access_token
    except KakaoException:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


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


@api_view(["GET"])
def kakao_callback(request):
    """
    Kakao callback
    """
    try:
        access_token = kakao_get_token(request)
        profile_json = kakao_get_profile(access_token)
        email = profile_json.get("kaccount_email", None)
        if email is None:
            raise KakaoException()
        properties = profile_json.get("properties")
        nickname = properties.get("nickname")
        # profile_image_url = properties.get("profile_image")
        # profile_image = requests.get(profile_image_url)

        user, created = User.objects.get_or_create(
            email=email,
            username=email,
            first_name=nickname,
            # avatar=profile_image,
            login_method=User.LOGIN_KAKAO,
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
            if user.login_method == User.LOGIN_KAKAO:
                encoded_jwt = jwt.encode(
                    {"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256"
                )
                return Response(data={"token": encoded_jwt, "id": user.pk})
            else:
                raise KakaoException()

    except KakaoException:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
