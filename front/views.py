from django.shortcuts import render

import requests


def homeView(request):
    api_url = "http://feud72.hopto.org/api/v1/"
    api_endpoint = "books/"
    url = api_url + api_endpoint
    raw = requests.get(url)
    raw_json = raw.json()
    book_list = raw_json["results"]
    return render(request, "front/home.html", {"items": book_list})


def detailView(request, isbn):
    api_url = "http://feud72.hopto.org/api/v1/"
    api_endpoint = "books/"
    url = api_url + api_endpoint + isbn
    raw = requests.get(url)
    raw_json = raw.json()
    book_detail = raw_json
    return render(request, "front/detail.html", {"item": book_detail})


def loginView(request):
    return render(request, "front/login.html")


def signupView(request):
    return render(request, "front/signup.html")