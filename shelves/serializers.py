from django.db.models import Avg

from rest_framework import serializers

from .models import MyBook

from books.models import Book
from users.models import User
from reviews.serializers import ReviewSerializer


class BookSerializer(serializers.ModelSerializer):
    avg_star = serializers.SerializerMethodField(required=False, read_only=True)

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
            "avg_star",
        )
        ref_name = "shelf_book_serializer"

    def get_avg_star(self, obj):
        avg = (
            Book.objects.filter(isbn=obj.isbn)
            .aggregate(Avg("review__star"))
            .get("review__star__avg")
        )
        if avg is None:
            return 0
        return avg


class MyBookSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    isbn = serializers.CharField(max_length=13, write_only=True)
    owner = serializers.SlugRelatedField(
        slug_field="nickname", queryset=User.objects.all(), required=False
    )
    review = ReviewSerializer(
        many=True, read_only=True, required=False, source="book.review_set"
    )

    class Meta:
        model = MyBook
        fields = (
            "id",
            "created_at",
            "owner",
            "book",
            "isbn",
            "review",
        )
        read_only_fields = ("id", "created_at", "owner", "book", "review")
        depth = 1
        ref_name = "shelf_mybook_serializer"

    def validate_isbn(self, value):
        request = self.context.get("request", None)
        owner = request.user
        if len(value) != 13:
            raise serializers.ValidationError("ISBN은 13글자 숫자로 이루어진 문자열이어야 합니다.")
        if MyBook.objects.filter(book__pk=value, owner__username=owner).exists():
            raise serializers.ValidationError("책장에 이미 존재하는 책입니다.")
        if not Book.objects.filter(isbn=value).exists():
            raise serializers.ValidationError("잘못된 ISBN입니다.")
        try:
            int(value)
        except ValueError:
            raise serializers.ValidationError("ISBN은 13글자 숫자로 이루어진 문자열이어야 합니다.")

    def create(self, validate_data):
        request = self.context.get("request", None)
        isbn = self.initial_data["isbn"]
        book = Book.objects.get(isbn=isbn)
        mybook = MyBook(book=book, owner=request.user)
        mybook.save()
        return mybook
