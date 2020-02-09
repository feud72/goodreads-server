import os
import datetime
import html

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
    raw_json = html.unescape(raw_json)
    data = raw_json["response"]["docs"][:10]
    return data


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
    data = processingData(data)
    return data


def processingData(data):
    if isinstance(data, dict):
        if "book" in data:
            data = data["book"]
        elif "doc" in data:
            data = data["doc"]
        title = data["bookname"]
        isbn = data["isbn13"]
        author = data["authors"]
        publisher = data["publisher"]
        pub_year = data["publication_date"]
        kdc = data["class_no"]
        description = data["description"]
        description = html.unescape(description)

        if "vol" in data:
            volume = data["vol"]
        else:
            volume = ""
        dic = {
            "title": title,
            "isbn": isbn,
            "author": author,
            "publisher": publisher,
            "pub_year": pub_year,
            "kdc": kdc,
            "description": description,
            "volume": volume,
        }
        return dic
    else:
        return dict()


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
    raw_json = html.unescape(raw_json)

    data_list = raw_json["response"]["docs"][:10]
    result = list()
    for data in data_list:
        isbn = data["book"]["isbn13"]
        title = data["book"]["bookname"]
        author = data["book"]["authors"]
        item = {"item": {"isbn": isbn, "title": title, "author": author}}
        result.append(item)
    return result


def getAnalysis(isbn="9788954655972"):
    url = LIB_BASE_URL + LIB_API_ENDPOINT["analysis"]
    params = {
        "authKey": LIB_AUTH_KEY,
        "isbn13": isbn,
        "format": "json",
    }
    raw = requests.get(url=url, params=params)
    raw_json = raw.json()
    raw_json = html.unescape(raw_json)
    return raw_json


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
    raw_json = html.unescape(raw_json)
    print(raw_json["response"])
    if "items" in raw_json["response"]:
        data = raw_json["response"]["items"][:10]

        return data
    else:
        return []


def kakaoSearch(query, page=1):
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
    params = {"target": "title", "query": query, "page": page}
    headers = {"Authorization": f"KakaoAK {KAKAO_KEY}"}
    raw = requests.get(url=url, params=params, headers=headers)
    raw_json = raw.json()
    raw_json = html.unescape(raw_json)
    data_list = raw_json["documents"]
    result = list()
    for data in data_list:
        isbn = data["isbn"].split(" ")[1]
        title = data["title"]
        author = ", ".join(data["authors"])
        description = data["contents"]
        item = {
            "item": {
                "isbn": isbn,
                "title": title,
                "author": author,
                "description": description,
            }
        }
        result.append(item)
    return result
