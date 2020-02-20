from django.core.files.base import ContentFile

from rest_framework import serializers
import requests

from .models import Book

from utils.get_data import getDetail
from reviews.serializers import ReviewSerializer


class BookSerializer(serializers.ModelSerializer):
    isbn = serializers.CharField(max_length=13, required=True)
    review = ReviewSerializer(
        many=True, read_only=True, required=False, source="review_set"
    )

    class Meta:
        model = Book
        fields = (
            "title",
            "author",
            "publisher",
            "pub_year",
            "isbn",
            "description",
            "bookImage",
            "review",
        )
        read_only_fields = (
            "title",
            "author",
            "publisher",
            "pub_year",
            "description",
            "bookImage",
            "review",
        )

    def validate_isbn(self, value):
        if len(value) != 13:
            raise serializers.ValidationError("ISBN must be 13 length.")
        if Book.objects.filter(isbn=value).exists():
            raise serializers.ValidationError("Already exists.")
        try:
            int(value)
        except ValueError:
            raise serializers.ValidationError("Not an integer.")

    def save(self):
        isbn = self.initial_data["isbn"]
        try:
            data = getDetail(isbn)
            bookImageURL = data.pop("bookImageURL")
            obj = Book.objects.create(**data)
            if bookImageURL:
                bookImage_raw = requests.get(bookImageURL)
                bookImage = ContentFile(bookImage_raw.content)
                obj.bookImage.save(f"{isbn}.jpg", bookImage)
            return obj
        except Exception:
            raise serializers.ValidationError({"isbn": "Invalid ISBN number."})
