from rest_framework import serializers

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "user", "book", "star", "description"]
        read_only_fields = ("id",)
        depth = 1
