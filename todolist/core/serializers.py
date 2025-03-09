from rest_framework import serializers
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from core.helpers import create_jwt, decode_jwt
from django.db.models import Q
# from django.core.exceptions


class AuthSerializer(serializers.Serializer):
    def to_representation(self, instance):
        # return access_token and refresh_toekn in response
        data = super().to_representation(instance)
        user_id = instance.id
        payload = {'user_id': user_id}
        data['user_id'] = user_id
        data['access_token'] = create_jwt(payload=payload, expires_in=3600)
        data['refresh_token'] = create_jwt(
            payload=payload, expires_in=3600 * 24 * 7)
        data.pop('username', None)
        return data


class RegisterSerializer(AuthSerializer, serializers.Serializer):
    username = serializers.CharField(min_length=8, max_length=25)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField()
    last_name = serializers.CharField(required=False)

    def validate(self, data):
        if User.objects.filter(Q(username=data['username']) | Q(email=data['email'])).exists():
            raise serializers.ValidationError(
                "User with given username or email already exists.")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(AuthSerializer, serializers.Serializer):
    username = serializers.CharField(min_length=8, max_length=25)
    password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        request = self.context.get('request')
        user = authenticate(request=request,
                            username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        return user


class RefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate_refresh_token(self, token):
        is_decoded, data = decode_jwt(token)
        if not is_decoded:
            raise serializers.ValidationError(f'{data}. Please login again')
        return data  # data is user_id

    def to_representation(self, instance):
        user_id = super().to_representation(instance)
        data = {}
        data['access_token'] = create_jwt({'user_id': user_id}, 3600)
        return data
