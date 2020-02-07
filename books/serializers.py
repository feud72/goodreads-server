from rest_framework import serializers

from .models import Book

from utils.get_data import getDetail


class BookSerializer(serializers.ModelSerializer):
    isbn = serializers.CharField(max_length=13, required=True)
    #    title = serializers.CharField(required=False, max_length=500, default="")
    #    author = serializers.CharField(required=False, max_length=200, default="")
    #    publisher = serializers.CharField(required=False, max_length=100, default="")
    #    pub_year = serializers.CharField(required=False, max_length=20, default="")
    #    volume = serializers.CharField(required=False, max_length=10, default="")
    #    kdc = serializers.CharField(required=False, max_length=10, default="")
    #    description = serializers.CharField(required=False, max_length=1000, default="")

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
            raise serializers.ValidationError("ISBN must be 13 length.")
        if Book.objects.filter(isbn=value).exists():
            raise serializers.ValidationError("Already exists.")
        try:
            int(value)
        except ValueError:
            raise serializers.ValidationError("Not an integer.")

    def save(self):
        isbn = self.initial_data["isbn"]
        print(isbn)
        data = getDetail(isbn)
        print(data)
        obj = Book.objects.create(**data)
        return obj
