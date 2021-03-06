from django.contrib.auth import password_validation, authenticate, get_user_model
from django.contrib.auth.models import BaseUserManager

from rest_framework import serializers

from users.models import User
from utils.username import get_random_name


class LoginSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "email",
            "password",
        )

    def validate_email(self, value):
        email = value
        user = get_user_model().objects.filter(email=email).exists()
        if not user:
            raise serializers.ValidationError("등록되지 않은 이메일입니다.")
        return BaseUserManager.normalize_email(value)

    def validate_password(self, value):
        username = self.initial_data["email"]
        password = self.initial_data["password"]
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("잘못된 비밀번호입니다.")
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
            raise serializers.ValidationError("이미 등록된 이메일입니다.")
        return BaseUserManager.normalize_email(value)

    def validate_password1(self, value):
        password_validation.validate_password(value)
        return value

    def validate_password2(self, value):
        if value != self.initial_data["password1"]:
            raise serializers.ValidationError("두 패스워드는 서로 일치해야 합니다.")
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
        nickname = get_random_name()
        user = get_user_model().objects.create_user(
            username=username, email=email, password=password, nickname=nickname
        )
        user.set_password(password)
        user.save()
        return user
