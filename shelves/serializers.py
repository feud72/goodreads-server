from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import MyBook, Memo

from books.models import Book
from books.serializers import BookSerializer


class MyBookSerializer(serializers.ModelSerializer):
    isbn = serializers.CharField(max_length=13, write_only=True)
    book = BookSerializer(many=True, read_only=True)

    class Meta:
        model = MyBook
        fields = ("id", "owner", "book", "isbn", "finished", "star")
        read_only_fields = ("id", "owner", "book", "finished", "star")

    def validate_isbn(self, value):
        if len(value) != 13:
            raise serializers.ValidationError("ISBN must be 13 length.")
        if MyBook.objects.filter(book__pk=value).exists():
            raise serializers.ValidationError("책장에 이미 존재하는 책입니다.")
        if not Book.objects.filter(isbn=value).exists():
            raise serializers.ValidationError("Invalid ISBN number.")
        try:
            int(value)
        except ValueError:
            raise serializers.ValidationError("Not an integer.")

    def save(self):
        isbn = self.initial_data["isbn"]
        username = self.initial_data["username"]
        try:
            owner = get_user_model().objects.get(username=username)
            self.validate_isbn(isbn)
            book = Book.objects.get(isbn=isbn)
            obj = MyBook.objects.create(owner=owner, book=book)
            return obj
        except Exception:
            raise serializers.ValidationError({"error": "Whoo."})


class MemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memo
        exclude = ()
