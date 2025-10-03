# serializers.py
from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    # use custom validotor for username to aviod django's validator
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all(), message="User with this nickname already exists.")]
    )
    class Meta:
        model = User
        fields = ("username", "password", "password2")
        extra_kwargs = {
            "password": {"write_only": True}
        }
        
    def validate_username(self, value: str):
        if len(value) > 15:
            raise serializers.ValidationError("Nickname length should not exceed 15 characters.")
        if len(value) < 3:
            raise serializers.ValidationError("Nickname must contain at least 3 characters")
        return value

    def validate(self, data): # type: ignore
        if " " in data["password"]:
            raise serializers.ValidationError("Password cannot contain spaces")
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Passwords don't match")
        return data

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=15, write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data): # type: ignore
        # Проверка есть ли пользователь с такими данными
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid login or password")
        data['user'] = user
        return data

class UserLoginVefificationSerializer(serializers.Serializer):
    code = serializers.CharField()

    def validate(self, data): # type: ignore
        if len(data['code']) != 6:
            raise serializers.ValidationError("Code must be 6 digits")
        return data


class UserEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
