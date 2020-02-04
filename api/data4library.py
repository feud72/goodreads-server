import os
import datetime
import requests

# from rest_framework.decorators import api_view

API_BASEURL = os.environ("LIB_BASEURL")

API_ENDPOINT = {
    "popular": "loanItemSrch",
    "recommend": "recommandList",
    "detail": "srchDtlList",
    "keyword": "keywordList",
}

AUTH_KEY = os.environ("LIB_KEY")


# @api_view(["GET"])
def popular():
    url = API_BASEURL + API_ENDPOINT["popular"]
    params = {
        "authKey": AUTH_KEY,
        "startDt": str(datetime.date.today() - datetime.timedelta(days=30)),
        "endDt": str(datetime.date.today()),
        "format": "json",
        "pageSize": 10,
    }
    req = requests.get(url=url, params=params)
    print(req.json())
