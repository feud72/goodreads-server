from rest_framework import serializers
from .models import User

from books.models import Book
from shelves.models import MyBook
from reviews.serializers import ReviewSerializer


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "isbn",
            "title",
            "author",
            "pub_year",
            "description",
            "num_views",
            "bookImage",
            "like_count",
            "review_count",
        )
        ref_name = "user_book_serializer"


class MyBookSerializer(serializers.ModelSerializer):

    book = BookSerializer(read_only=True,)

    class Meta:
        model = MyBook
        fields = ("id", "created_at", "book")


class UserSerializer(serializers.ModelSerializer):
    mybook = MyBookSerializer(
        many=True, read_only=True, required=False, source="mybook_set"
    )
    review = ReviewSerializer(
        many=True, read_only=True, required=False, source="review_set"
    )

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "nickname",
            "created_at",
            "mybook",
            "review",
        )
        read_only_fields = (
            "id",
            "created_at",
            "mybook",
            "review",
        )
        depth = 1
