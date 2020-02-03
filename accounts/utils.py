from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers


def get_and_authenticate_user(email, password):
    user = authenticate(username=email, password=password)
    if user is None:
        raise serializers.ValidationError("Invalid username/password.")
    return user


def create_user_account(username, email, password, **extra_fields):
    user = get_user_model().objects.create_user(
        username=username, email=email, password=password, **extra_fields
    )
    return user
