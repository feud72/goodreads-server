import os
import random

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


def getDetail(isbn=None):
    data = kakaoSearch(isbn)[0]
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
    if "docs" in raw_json["response"]:
        data_list = raw_json["response"]["docs"][:25]
        sample_size = 10 if len(data_list) >= 10 else len(data_list)
        data_list = random.sample(data_list, sample_size)
        result = list()
        for data in data_list:
            data = data["book"]
            isbn = data["isbn13"]
            title = data["bookname"]
            author = data["authors"]
            pub_year = data["publication_year"]
            item = {
                "isbn": isbn,
                "title": title,
                "author": author,
                "pub_year": pub_year,
            }
            result.append(item)
        return result
    else:
        return []


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
    if "items" in raw_json["response"]:
        data = raw_json["response"]["items"][:10]

        return data
    else:
        return []


def kakaoSearch(query, page=1):
    url = KAKAO_BOOK_URL
    params = {"target": "title", "query": query, "page": page}
    headers = {"Authorization": f"KakaoAK {KAKAO_KEY}"}
    raw = requests.get(url=url, params=params, headers=headers)
    raw_json = raw.json()
    data_list = raw_json["documents"]
    result = list()
    for data in data_list:
        isbn = data["isbn"].split(" ")[1]
        title = data["title"]
        author = ", ".join(data["authors"])
        publisher = data["publisher"]
        pub_year = data["datetime"][0:4]
        description = data["contents"] if data["contents"] else ""
        if len(description) > 200:
            description = description + " ..."
        bookImage = data["thumbnail"] if data["thumbnail"] else ""
        item = {
            "isbn": isbn,
            "title": title,
            "author": author,
            "publisher": publisher,
            "pub_year": pub_year,
            "description": description,
            "bookImage": bookImage,
        }
        result.append(item)
    return result
