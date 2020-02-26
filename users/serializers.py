from rest_framework import serializers
from .models import User

from shelves.serializers import MyBookSerializer
from reviews.serializers import ReviewSerializer


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
