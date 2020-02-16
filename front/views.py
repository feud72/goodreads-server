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
    return render(request, "front/home.html", {**login})


def recentView(request):
    login = loginStatus(request)
    endpoint = "api/v1/books/"
    raw = getAPI(API_URL, endpoint)
    book_list = raw["results"]
    return render(request, "front/recent.html", {"items": book_list, **login})


def popularView(request):
    login = loginStatus(request)
    endpoint = "api/v1/books/recommend/"
    raw = getAPI(API_URL, endpoint)
    book_list = raw
    return render(request, "front/popular.html", {"items": book_list, **login})


def detailView(request, isbn):
    login = loginStatus(request)
    endpoint = "api/v1/books/"
    raw = getAPI(API_URL, endpoint, isbn)
    book_detail = raw
    recommend_url = "recommend/"
    raw = getAPI(API_URL, endpoint, isbn, "/", recommend_url)
    recommend_data = raw
    return render(
        request,
        "front/detail.html",
        {"item": book_detail, "recommend": recommend_data, **login},
    )


def shelfView(request):
    login = loginStatus(request)
    if login["status"] is True:
        token = login["token"]
        endpoint = "api/v1/shelves/"
        url = API_URL + endpoint
        headers = {"Authorization": f"Token {token}"}
        raw = requests.get(url, headers=headers)
        print(raw.text)
        if raw.status_code == 200:
            raw_json = raw.json()
            items = raw_json["results"]
            return render(request, "front/shelf.html", {"items": items, **login})
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
            endpoint = "api/v1/shelves/"
            url = API_URL + endpoint
            headers = {"Authorization": f"Token {token}"}
            raw = requests.post(url, data={"isbn": isbn}, headers=headers)
            if raw.status_code == 200:
                raw_json = raw.json()
                items = raw_json["results"]
                return render(request, "front/shelf.html", {"items": items, **login})
    return render(request, "front/shelf.html", login)


def searchView(request):
    login = loginStatus(request)
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            term = form.cleaned_data["term"]
            endpoint = "api/v1/books/search/"
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
            url = API_URL + "api/v1/accounts/login/"
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
            url = API_URL + "api/v1/accounts/signup/"
            req = requests.post(
                url, {"email": email, "password1": password1, "password2": password2}
            )
            if req.status_code == 201:
                res = req.json()
                return render(request, str(res))
            else:
                return render(request, "front/signup.html", {"form": form})
    return redirect(reverse("front:signup"))


def logoutView(request):
    response = HttpResponseRedirect(reverse("front:home"))
    response.delete_cookie("token", domain=settings.COOKIE_DOMAIN)
    return response
