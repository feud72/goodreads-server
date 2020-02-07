from rest_framework import serializers

from .models import Book


class BookSerializer(serializers.ModelSerializer):
    isbn = serializers.CharField(max_length=13, required=True)

    class Meta:
        model = Book
        fields = (
            "title",
            "author",
            "publisher",
            "pub_year",
            "volume",
            "isbn",
            "kdc",
            "description",
        )
        read_only_fields = (
            "title",
            "author",
            "publisher",
            "pub_year",
            "volume",
            "kdc",
            "description",
        )

    def validate_isbn(self, value):
        if len(value) != 13:
            raise serializers.ValidationError("ISBN must be 13 length string")
        try:
            int(value)
        except ValueError:
            raise serializers.ValidationError("Not an integer")
