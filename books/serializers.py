from django.core.files.base import ContentFile

from rest_framework import serializers
import requests

from .models import Book

from utils.get_data import getDetail
from reviews.serializers import ReviewSerializer
from keywords.serializers import KeywordSerializer


class BookSerializer(serializers.ModelSerializer):
    isbn = serializers.CharField(max_length=13, required=True)
    review = ReviewSerializer(
        many=True, read_only=True, required=False, source="review_set"
    )
    keywords = KeywordSerializer(
        many=True, read_only=True, required=False, source="keyword_set"
    )
    like_count = serializers.IntegerField(required=False)
    review_count = serializers.IntegerField(required=False)
    avg_star = serializers.FloatField(required=False)

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
            "keywords",
            "num_views",
            "like_count",
            "review_count",
            "avg_star",
        )
        read_only_fields = (
            "title",
            "author",
            "publisher",
            "pub_year",
            "description",
            "bookImage",
            "review",
            "num_views",
            "like_count",
            "review_count",
            "avg_star",
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

    def create(self, validate_data):
        isbn = self.initial_data["isbn"]
        data = getDetail(isbn)
        bookImageURL = data.pop("bookImageURL")
        book = Book.objects.create(**data)
        if bookImageURL:
            bookImage_raw = requests.get(bookImageURL)
            bookImage = ContentFile(bookImage_raw.content)
            book.bookImage.save(f"{isbn}.jpg", bookImage)
            book.save()
        return book
