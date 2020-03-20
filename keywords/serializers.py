from rest_framework import serializers

from .models import Keyword

from books.models import Book


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = (
            "word",
            "weight",
        )
        read_only_fields = (
            "word",
            "weight",
        )


class SmallBookSerializer(serializers.ModelSerializer):
    keywords = KeywordSerializer(source="keyword_set", many=True)

    class Meta:
        model = Book
        fields = (
            "isbn",
            "title",
            "bookImage",
            "description",
            "author",
            "pub_year",
            "keywords",
        )


class RelatedBookSerializer(serializers.ModelSerializer):
    book = SmallBookSerializer(read_only=True)

    class Meta:
        model = Keyword
        fields = ("book", "weight")
