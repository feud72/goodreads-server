from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import MyBook, Review

from books.models import Book
from books.serializers import BookSerializer


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.SlugRelatedField(read_only=True, slug_field="mybook__owner")

    class Meta:
        model = Review
        fields = ["reviewer", "book", "star", "description"]


class MyBookSerializer(serializers.ModelSerializer):
    isbn = serializers.CharField(max_length=13, write_only=True)
    book = BookSerializer(required=False)
    review = ReviewSerializer(required=False)

    class Meta:
        model = MyBook
        fields = (
            "id",
            "owner",
            "book",
            "isbn",
            "review",
        )
        read_only_fields = ("id", "owner", "book")

    def validate_isbn(self, value):
        owner = self.initial_data["username"]
        if len(value) != 13:
            raise serializers.ValidationError("ISBN must be 13 length.")
        if MyBook.objects.filter(book__pk=value, owner__username=owner).exists():
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
            current_book = Book.objects.get(isbn=isbn)
            obj = MyBook.objects.create(owner=owner, book=current_book)
            return obj
        except Exception:
            raise serializers.ValidationError({"error": "Whoo."})
