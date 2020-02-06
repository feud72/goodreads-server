from django.contrib.auth import password_validation, authenticate, get_user_model
from django.contrib.auth.models import BaseUserManager

from rest_framework import serializers

from users.models import User
from shelves.models import BookShelf


class LoginSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "password",
        )

    def validate(self, value):
        username = self.initial_data["email"]
        password = self.initial_data["password"]
        if not username:
            raise serializers.ValidationError({"error": "Username field is required."})
        if not password:
            raise serializers.ValidationError({"error": "Password field is required."})
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(
                {"error": "Email and Password don't match."}
            )
        else:
            return value


class RegistrationSerializer(serializers.ModelSerializer):

    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            # "id",
            "email",
            "password1",
            "password2",
        )
        # read_only_fields = ("id")

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
        user = get_user_model().objects.create_user(
            username=username, email=email, password=password,
        )
        bookshelf = BookShelf.objects.create(owner=user)
        user.current_bookshelf = bookshelf
        user.set_password(password)
        user.save()
        return user
