from rest_framework import serializers

from .models import Review

from users.serializers import UserSerializer
from books.models import Book


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = Review
        fields = ["id", "user", "book", "star", "description"]
        read_only_fields = ("id",)
        depth = 1

    def create(self, validated_data):
        request = self.context.get("request", None)
        review = Review(
            book=validated_data["book"],
            star=validated_data["star"],
            description=validated_data["description"],
            user=request.user,
        )
        review.save()
        return review
