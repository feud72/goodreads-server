from django.db.models import Avg
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
    avg_star = serializers.FloatField(required=False, read_only=True)

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

    def get_avg_star(self, obj):
        avg = (
            Book.objects.filter(isbn=obj.isbn)
            .aggregate(Avg("review__star"))
            .get("review__star__avg")
        )
        if avg is None:
            return 0
        return avg

    def validate_isbn(self, value):
        if len(value) != 13:
            raise serializers.ValidationError("ISBN은 13글자 숫자로 이루어진 문자열이어야 합니다.")
        if Book.objects.filter(isbn=value).exists():
            raise serializers.ValidationError("이미 존재하는 ISBN입니다.")
        try:
            int(value)
        except ValueError:
            raise serializers.ValidationError("ISBN은 13글자 숫자로 이루어진 문자열이어야 합니다.")

    def create(self, validate_data):
        isbn = self.initial_data["isbn"]
        data = getDetail(isbn)
        bookImageURL = data.pop("bookImage")
        book = Book.objects.create(**data)
        if bookImageURL:
            bookImage_raw = requests.get(bookImageURL)
            bookImage = ContentFile(bookImage_raw.content)
            book.bookImage.save(f"{isbn}.jpg", bookImage)
            book.save()
        return book
