from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "nickname", "current_bookshelf")
        read_only_fields = ("id",)
