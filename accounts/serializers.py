import random

from django.contrib.auth import password_validation, authenticate, get_user_model
from django.contrib.auth.models import BaseUserManager

from rest_framework import serializers

from users.models import User


class LoginSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "email",
            "password",
        )

    def validate(self, value):
        username = self.initial_data["email"]
        password = self.initial_data["password"]
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid Email / Password.")
        else:
            return value


class RegistrationSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "email",
            "password1",
            "password2",
        )

    def validate_email(self, value):
        email = value
        user = get_user_model().objects.filter(email=email)
        if user:
            raise serializers.ValidationError("Email is already taken.")
        return BaseUserManager.normalize_email(value)

    def validate_password1(self, value):
        password_validation.validate_password(value)
        return value

    def validate_password2(self, value):
        if value != self.initial_data["password1"]:
            raise serializers.ValidationError("Passwords must match.")
        return value

    def create(self, validated_data):
        password = validated_data.get("password1")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user

    def save(self):
        email = self.validated_data["email"]
        username = email
        password = self.validated_data["password1"]
        name = random.choice(
            [
                "철수",
                "영희",
                "니꼬",
                "린",
                "톰 크루즈",
                "해리 포터",
                "수지",
                "다람쥐",
                "스칼렛 요한슨",
                "곽철용",
                "카피추",
                "빌 게이츠",
            ]
        )
        deco = random.choice(
            [
                "배고픈",
                "행복한",
                "두근두근한",
                "멋진",
                "힘찬",
                "갓갓",
                "놀란",
                "한 끗으로 5억을 태운",
                "욕심이 전혀 없는",
                "격렬하게 쉬고 싶은",
            ]
        )
        nickname = f"{deco} {name}"
        user = get_user_model().objects.create_user(
            username=username, email=email, password=password, nickname=nickname
        )
        user.set_password(password)
        user.save()
        return user
