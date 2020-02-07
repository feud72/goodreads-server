import os
import datetime
import requests

LIB_BASE_URL = os.environ.get("LIB_BASE_URL")
LIB_API_ENDPOINT = {
    "popular": "loanItemSrch",
    "recommend": "recommandList",
    "keyword": "keywordList",
    "analysis": "usageAnalysisList",
    "detail": "srchDtlList",
}
LIB_AUTH_KEY = os.environ.get("LIB_KEY")

KAKAO_KEY = os.environ.get("KAKAO_ID")
KAKAO_BOOK_URL = "https://dapi.kakao.com/v3/search/book"


def getPopular():
    url = LIB_BASE_URL + LIB_API_ENDPOINT["popular"]
    params = {
        "authKey": LIB_AUTH_KEY,
        "startDt": str(datetime.date.today() - datetime.timedelta(days=30)),
        "endDt": str(datetime.date.today()),
        "format": "json",
        "pageSize": 10,
    }
    raw = requests.get(url=url, params=params)
    raw_json = raw.json()
    data = raw_json["response"]["docs"][:10]
    return data


def getRecommendByISBN(isbn=None):
    if isbn is None:
        raise ValueError("ISBN is required")
    url = LIB_BASE_URL + LIB_API_ENDPOINT["recommend"]
    params = {
        "authKey": LIB_AUTH_KEY,
        "isbn13": isbn,
        "format": "json",
    }
    raw = requests.get(url=url, params=params)
    raw_json = raw.json()
    data = raw_json["response"]["docs"][:10]
    return data


def getAnalysis(isbn="9788954655972"):
    url = LIB_BASE_URL + LIB_API_ENDPOINT["analysis"]
    params = {
        "authKey": LIB_AUTH_KEY,
        "isbn13": isbn,
        "format": "json",
    }
    raw = requests.get(url=url, params=params)
    raw_json = raw.json()
    return raw_json


def getDetail(isbn=None):
    if isbn is None:
        raise ValueError("ISBN is required")
    url = LIB_BASE_URL + LIB_API_ENDPOINT["detail"]
    params = {
        "authKey": LIB_AUTH_KEY,
        "isbn13": isbn,
        "format": "json",
    }
    raw = requests.get(url=url, params=params)
    raw_json = raw.json()
    data = raw_json["response"]["detail"][0]
    return data


def getKeywordList(isbn=None):
    if isbn is None:
        raise ValueError("ISBN is required")
    url = LIB_BASE_URL + LIB_API_ENDPOINT["keyword"]
    params = {
        "authKey": LIB_AUTH_KEY,
        "isbn13": isbn,
        "format": "json",
    }
    raw = requests.get(url=url, params=params)
    raw_json = raw.json()
    data = raw_json["response"]["items"][:10]
    return data


def kakaoSearch(query):
    """
    argument
      query : string
    return
      result : list [ dict{
      "isbn": string,
      "title": string,
      } ]
    """
    url = KAKAO_BOOK_URL
    params = {"target": "title", "query": query}
    headers = {"Authorization": f"KakaoAK {KAKAO_KEY}"}
    raw = requests.get(url=url, params=params, headers=headers)
    raw_json = raw.json()
    data_list = raw_json["documents"]
    result = list()
    for data in data_list:
        isbn = data["isbn"].split(" ")[1]
        title = data["title"]
        item = {"item": {"isbn": isbn, "title": title}}
        result.append(item)
    return result
