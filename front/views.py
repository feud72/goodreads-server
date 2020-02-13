import os

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings

import requests


def loginStatus(request):
    token = request.COOKIES.get("token", None)
    result = {"login": False}
    if token:
        result["login"] = True
    return result


def homeView(request):
    login = loginStatus(request)
    return render(request, "front/home.html", login)


def recentView(request):
    login = loginStatus(request)
    api_url = os.environ["BASE_URI"]
    api_endpoint = "api/v1/books/"
    url = api_url + api_endpoint
    raw = requests.get(url)
    raw_json = raw.json()
    book_list = raw_json["results"]
    return render(request, "front/recent.html", {"items": book_list, **login})


def popularView(request):
    login = loginStatus(request)
    api_url = os.environ["BASE_URI"]
    api_endpoint = "api/v1/books/recommend/"
    url = api_url + api_endpoint
    raw = requests.get(url)
    book_list = raw.json()
    return render(request, "front/popular.html", {"items": book_list, **login})


def detailView(request, isbn):
    api_url = os.environ["BASE_URI"]
    detail_endpoint = "api/v1/books/"
    detail_url = f"{api_url}{detail_endpoint}{isbn}/"
    raw = requests.get(detail_url)
    book_detail = raw.json()
    recommend_url = detail_url + "recommend/"
    raw = requests.get(recommend_url)
    recommend_data = raw.json()
    return render(
        request, "front/detail.html", {"item": book_detail, "recommend": recommend_data}
    )


def loginView(request):
    url = os.environ["BASE_URI"] + "api/v1/accounts/login/"
    req = requests.post(url, {"email": "user@example.com", "password": "string12"})
    res = req.json()
    token = res["token"]
    response = HttpResponseRedirect(reverse("front:home"))
    response.set_cookie(key="token", value=token, domain=settings.COOKIE_DOMAIN)
    return response


def logoutView(request):
    response = HttpResponseRedirect(reverse("front:home"))
    response.delete_cookie("token")
    return response
