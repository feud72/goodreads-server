import os

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings

import requests

from .forms import LoginForm, SearchForm, SignupForm, SubscribeForm

API_URL = os.environ["API_URI"]


def loginStatus(request):
    token = request.COOKIES.get("token", None)
    result = {"token": token, "status": False}
    if token:
        result["status"] = True
    return result


def getAPI(base, endpoint, *args):
    url = "".join((base, endpoint, *args))
    raw = requests.get(url)
    raw_json = raw.json()
    return raw_json


def homeView(request):
    login = loginStatus(request)
    endpoint = "/api/v1/books/"
    raw = getAPI(API_URL, endpoint)
    book_list = raw["results"][:3]
    return render(request, "front/home.html", {"items": book_list, **login})


def recentView(request):
    login = loginStatus(request)
    endpoint = "/api/v1/books/"
    raw = getAPI(API_URL, endpoint)
    book_list = raw["results"]
    return render(request, "front/recent.html", {"items": book_list, **login})


def popularView(request):
    login = loginStatus(request)
    endpoint = "/api/v1/books/recommend/"
    raw = getAPI(API_URL, endpoint)
    book_list = raw
    return render(request, "front/popular.html", {"items": book_list, **login})


def detailView(request, isbn):
    login = loginStatus(request)
    endpoint = "/api/v1/books/"
    raw = getAPI(API_URL, endpoint, isbn)
    book_detail = raw
    recommend_url = "/recommend/"
    raw = getAPI(API_URL, endpoint, isbn, recommend_url)
    recommend_data = raw
    return render(
        request,
        "front/detail.html",
        {"item": book_detail, "recommend": recommend_data, **login},
    )


def shelfView(request):
    login = loginStatus(request)
    if login["status"] is False:
        return redirect(reverse("front:login"))
    else:
        token = login["token"]
        endpoint = "/api/v1/shelves/"
        url = API_URL + endpoint
        headers = {"Authorization": f"Token {token}"}
        raw = requests.get(url, headers=headers)
        if raw.status_code == 200:
            raw_json = raw.json()
            items = raw_json["results"]
            return render(request, "front/shelf.html", {"items": items, **login})
        else:
            raw_text = raw.text
            return render(request, "front/shelf.html", {"errors": raw_text, **login})

    return render(request, "front/shelf.html", login)


def subscribeView(request):
    login = loginStatus(request)
    if login["status"] is not True:
        return redirect(reverse("front:login"))
    else:
        if request.method == "POST":
            form = SubscribeForm(request.POST)
            if form.is_valid():
                isbn = form.cleaned_data["isbn"]
            token = login["token"]
            endpoint = "/api/v1/shelves/"
            url = API_URL + endpoint
            headers = {"Authorization": f"Token {token}"}
            requests.post(url, data={"isbn": isbn}, headers=headers)
            return redirect(reverse("front:shelf"))


def searchView(request):
    login = loginStatus(request)
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            term = form.cleaned_data["term"]
            endpoint = "/api/v1/books/search/"
            url = API_URL + endpoint
            params = {"search": term}
            raw = requests.get(url, params=params)
            if raw.status_code == 200:
                raw_json = raw.json()
                return render(
                    request, "front/search.html", {"items": raw_json, **login}
                )
            else:
                return render(request, "Not Found", login)
    else:
        return render(request, "Bad Request.", login)


def loginView(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "front/login.html", {"form": form})
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            url = API_URL + reverse("accounts:login")
            req = requests.post(url, {"email": email, "password": password})
            res = req.json()
            if "message" in res:
                if res["message"] == "success":
                    token = res["token"]
                    response = HttpResponseRedirect(reverse("front:shelf"))
                    response.set_cookie(
                        key="token", value=token, domain=settings.COOKIE_DOMAIN
                    )
                    return response
            else:
                return render(request, "front/login.html", {"form": form})
    return redirect(reverse("front:login"))


def signupView(request):
    if request.method == "GET":
        form = SignupForm()
        return render(request, "front/signup.html", {"form": form})
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password1 = form.cleaned_data["password1"]
            password2 = form.cleaned_data["password2"]
            url = API_URL + "/api/v1/accounts/signup/"
            req = requests.post(
                url, {"email": email, "password1": password1, "password2": password2}
            )
            if req.status_code == 201:
                return redirect(reverse("front:login"))
            else:
                return render(request, "front/signup.html", {"form": form})
    return redirect(reverse("front:signup"))


def logoutView(request):
    response = HttpResponseRedirect(reverse("front:home"))
    response.delete_cookie("token", domain=settings.COOKIE_DOMAIN)
    return response


def kakaoLoginView(request):
    """
    카카오 로그인
    """
    client_id = os.environ.get("KAKAO_ID")
    redirect_uri = API_URL + reverse("front:kakaocallback")
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )


class KakaoException(Exception):
    pass


def kakao_get_token(request):
    try:
        client_id = os.environ.get("KAKAO_ID")
        code = request.GET.get("code")
        redirect_uri = API_URL + reverse("front:kakaocallback")
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
        return None


def kakaoCallbackView(request):
    """
    카카오 콜백
    """
    try:
        access_token = kakao_get_token(request)
        if access_token is None:
            raise KakaoException()
        else:
            endpoint = reverse("accounts:kakao")
            url = API_URL + endpoint
            data = {"token": access_token}
            req = requests.post(url, data=data)
            if req.status_code in (200, 201):
                res = req.json()
                token = res.get("token")
                response = HttpResponseRedirect(reverse("front:shelf"))
                response.set_cookie(
                    key="token", value=token, domain=settings.COOKIE_DOMAIN
                )
                return response
            else:
                return render(request, "Hing")
    except KakaoException:
        return render(request, "Hong")
