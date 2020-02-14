import os

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings

import requests

from .forms import LoginForm


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
    api_url = os.environ["API_URI"]
    api_endpoint = "api/v1/books/"
    url = api_url + api_endpoint
    raw = requests.get(url)
    raw_json = raw.json()
    book_list = raw_json["results"]
    return render(request, "front/recent.html", {"items": book_list, **login})


def popularView(request):
    login = loginStatus(request)
    api_url = os.environ["API_URI"]
    api_endpoint = "api/v1/books/recommend/"
    url = api_url + api_endpoint
    raw = requests.get(url)
    book_list = raw.json()
    return render(request, "front/popular.html", {"items": book_list, **login})


def detailView(request, isbn):
    api_url = os.environ["API_URI"]
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
    if request.method == "GET":
        form = LoginForm()
        return render(request, "front/login.html", {"form": form})
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            print(email, password)
            url = os.environ["API_URI"] + "api/v1/accounts/login/"
            req = requests.post(url, {"email": email, "password": password})
            res = req.json()
            if "message" in res:
                if res["message"] == "success":
                    token = res["token"]
                    response = HttpResponseRedirect(reverse("front:home"))
                    response.set_cookie(
                        key="token", value=token, domain=settings.COOKIE_DOMAIN
                    )
                    return response
            else:
                return render(request, "front/login.html", {"form": form})
    return redirect(reverse("front:login"))


def logoutView(request):
    response = HttpResponseRedirect(reverse("front:home"))
    response.delete_cookie("token")
    return response
