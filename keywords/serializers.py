from rest_framework import serializers

from .models import Keyword

from books.models import Book


class SmallBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "isbn",
            "title",
            "bookImage",
            "description",
            "author",
            "pub_year",
        )


class RelatedBookSerializer(serializers.ModelSerializer):
    book = SmallBookSerializer(read_only=True)

    class Meta:
        model = Keyword
        fields = ("book", "weight")


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = (
            "book",
            "word",
            "weight",
        )
        read_only_fields = (
            "book",
            "word",
            "weight",
        )
