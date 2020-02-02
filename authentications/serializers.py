from rest_framework import serializers
from users.models import User


class LoginSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
        )


class RegistrationSerializer(serializers.ModelSerializer):

    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "avatar",
            "password1",
            "password2",
        )
        read_only_fields = ("id", "avatar")

    def save(self):
        user = User(
            username=self.validated_data["username"], email=self.validated_data["email"]
        )
        password1 = self.validated_data["password1"]
        password2 = self.validated_data["password2"]
        if password1 != password2:
            raise serializers.ValidationError({"password": "Passwords must match."})
        else:
            user.set_password(password1)
            user.save()
            return user
