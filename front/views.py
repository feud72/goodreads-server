from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings

import requests


def homeView(request):
    api_url = "http://feud72.hopto.org/api/v1/"
    api_endpoint = "books/"
    url = api_url + api_endpoint
    raw = requests.get(url)
    raw_json = raw.json()
    book_list = raw_json["results"]
    return render(request, "front/home.html", {"items": book_list})


def popularView(request):
    api_url = "http://feud72.hopto.org/api/v1/"
    api_endpoint = "books/recommend/"
    url = api_url + api_endpoint
    raw = requests.get(url)
    book_list = raw.json()
    return render(request, "front/home.html", {"items": book_list})


def detailView(request, isbn):
    api_url = "http://feud72.hopto.org/api/v1"
    detail_endpoint = "books"
    detail_url = f"{api_url}/{detail_endpoint}/{isbn}/"
    raw = requests.get(detail_url)
    book_detail = raw.json()
    recommend_url = detail_url + "recommend/"
    raw = requests.get(recommend_url)
    recommend_data = raw.json()
    return render(
        request, "front/detail.html", {"item": book_detail, "recommend": recommend_data}
    )


def loginView(request):
    url = "http://feud72.hopto.org/api/v1/accounts/login/"
    req = requests.post(url, {"email": "user@example.com", "password": "string12"})
    res = req.json()
    token = res["token"]
    print(token)
    response = HttpResponseRedirect(reverse("front:home"))
    response.set_cookie(key="token", value=token, domain=settings.COOKIE_DOMAIN)
    return response


#    if request.method == "POST":
#        form = LoginForm(request.POST)
#        if form.is_valid():
#            email = form.cleaned_data["email"]
#            password = form.cleaned_data["password"]
#            url = "http://feud72.hopto.org/api/v1/accounts/login/"
#            req = requests.post(url, {"email": email, "password": password})
#            res = req.json()
#            if "message" in res:
#                if res["message"] == "success":
#                    token = res["token"]
#                    print(token)
#                    return redirect("front:home")
#            return render(request, "front/login.html")
#        else:
#            return redirect("front:login")
#    else:
#        form = LoginForm()
#        return render(request, "front/login.html", {"form": form})


def signupView(request):
    return render(request, "front/signup.html")
