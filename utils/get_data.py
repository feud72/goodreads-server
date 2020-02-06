import os
import datetime
import requests

API_BASE_URL = os.environ.get("LIB_BASE_URL")

API_ENDPOINT = {
    "popular": "loanItemSrch",
    "recommend": "recommandList",
    "keyword": "keywordList",
    "analysis": "usageAnalysisList",
    "detail": "srchDtlList",
}

AUTH_KEY = os.environ.get("LIB_KEY")


def getPopular():
    url = API_BASE_URL + API_ENDPOINT["popular"]
    params = {
        "authKey": AUTH_KEY,
        "startDt": str(datetime.date.today() - datetime.timedelta(days=30)),
        "endDt": str(datetime.date.today()),
        "format": "json",
        "pageSize": 10,
    }
    raw = requests.get(url=url, params=params)
    raw_json = raw.json()
    return raw_json


def getRecommend(isbn="9788954655972"):
    url = API_BASE_URL + API_ENDPOINT["recommend"]
    params = {"authKey": AUTH_KEY, "isbn13": isbn, "format": "json"}
    raw = requests.get(url=url, params=params)
    raw_json = raw.json()
    return raw_json


def getAnalysis(isbn="9788954655972"):
    url = API_BASE_URL + API_ENDPOINT["analysis"]
    params = {
        "authKey": AUTH_KEY,
        "isbn13": isbn,
        "format": "json",
    }
    raw = requests.get(url=url, params=params)
    raw_json = raw.json()
    return raw_json


def getDetail(isbn="9788954655972"):
    url = API_BASE_URL + API_ENDPOINT["detail"]
    params = {
        "authKey": AUTH_KEY,
        "isbn13": isbn,
        "format": "json",
    }
    raw = requests.get(url=url, params=params)
    raw_json = raw.json()
    data = raw_json["response"]["detail"][0]
    return data


def getKeywordList(isbn="9788937473135"):
    url = API_BASE_URL + API_ENDPOINT["keyword"]
    params = {
        "authKey": AUTH_KEY,
        "isbn13": isbn,
        "format": "json",
    }
    raw = requests.get(url=url, params=params)
    raw_json = raw.json()
    data = raw_json["response"]["items"]
    return data
