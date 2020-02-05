from rest_framework import serializers

from .models import BookShelf, MyBook, Memo


class BookShelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookShelf
        exclude = ()


class MyBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyBook
        exclude = ()


class MemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memo
        exclude = ()
