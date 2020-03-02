import time

from .models import Book

from keywords.models import Keyword
from utils.get_data import getKeywordList


def create_keywords(isbn):
    if Keyword.objects.filter(book__isbn=isbn).exists():
        print("Already exists.")
        return
    instance_is_exist = Book.objects.filter(isbn=isbn).exists()
    if instance_is_exist:
        instance = Book.objects.get(isbn=isbn)
        keyword_list = getKeywordList(isbn)
        if not keyword_list:
            return
        for keyword in keyword_list:
            keyword = keyword["item"]
            word = keyword["word"]
            weight = keyword["weight"]
            print(word, weight)
            Keyword.objects.create(book=instance, word=word, weight=weight)
            time.sleep(0.1)
    else:
        print("Nooooo")
