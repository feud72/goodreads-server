import os

from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import login

import requests

from users.models import User


def kakao_login(request):
    client_id = os.environ.get("KAKAO_ID")
    redirect_uri = "http://127.0.0.1:8000/api/v1/accounts/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        client_id = os.environ.get("KAKAO_ID")
        code = request.GET.get("code")
        redirect_uri = "http://127.0.0.1:8000/api/v1/accounts/login/kakao/callback"
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        )
        token_json = token_request.json()
        print(token_json)
        error = token_json.get("error", None)
        if error is not None:
            raise KakaoException()
        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v1/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        email = profile_json.get("kaccount_email", None)
        if email is None:
            raise KakaoException()
        properties = profile_json.get("properties")
        nickname = properties.get("nickname")
        profile_image = properties.get("profile_image")
        try:
            user = User.objects.get(email=email)
            if user.login_method != User.LOGIN_KAKAO:
                raise KakaoException()
        except User.DoesNotExist:
            user = User.objects.create(
                email=email,
                username=email,
                first_name=nickname,
                avatar=profile_image,
                login_method=User.LOGIN_KAKAO,
            )
            user.set_unusable_password()
            user.save()
        login(request, user)
        return redirect(reverse("accounts:login"))
    except KakaoException:
        return redirect(reverse("users:login"))
