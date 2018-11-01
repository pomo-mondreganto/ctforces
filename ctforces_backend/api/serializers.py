from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_core_exceptions
from rest_framework import serializers as rest_serializers

from api import models as api_models


class UserCreateSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = api_models.User
        fields = (
            'username', 'email', 'password'
        )
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'username': {
                'validators': [api_models.User.username_validator]
            },
        }

    @staticmethod
    def validate_email(value):
        new_email = value.lower()
        if api_models.User.objects.filter(email=new_email).exists():
            raise rest_serializers.ValidationError('User with this email is already registered.')
        return new_email

    def validate(self, data):
        user = api_models.User(**data)
        password = data.get('password')

        errors = dict()
        try:
            validate_password(password=password, user=user)
        except django_core_exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise rest_serializers.ValidationError(errors)

        return data

    def create(self, validated_data):
        user = api_models.User.objects.create_user(**validated_data, is_active=False)
        return user


class UserBasicSerializer(rest_serializers.ModelSerializer):
    avatar_main = rest_serializers.URLField(source='avatar.main.url')
    avatar_small = rest_serializers.URLField(source='avatar.small.url')
    cost_sum = rest_serializers.IntegerField(read_only=True)

    class Meta:
        model = api_models.User
        fields = (
            'id',
            'username',
            'rating',
            'max_rating',
            'cost_sum',
            'avatar_main',
            'avatar_small',
        )


class UserMainSerializer(rest_serializers.ModelSerializer):
    cost_sum = rest_serializers.IntegerField(read_only=True)
    avatar_main = rest_serializers.URLField(source='avatar.main.url', read_only=True)
    avatar_small = rest_serializers.URLField(source='avatar.small.url', read_only=True)

    class Meta:
        model = api_models.User
        fields = (
            'id',
            'username',
            'email',
            'rating',
            'max_rating',
            'cost_sum',
            'avatar_main',
            'avatar_small',
            'first_name',
            'last_name',
            'password',
        )

        extra_kwargs = {
            'password': {
                'write_only': True,
            },
            'email': {
                'read_only': True,
            },
        }

    def validate(self, data):
        user = api_models.User(**data)
        password = data.get('password')
        if not password:
            if password is not None:
                data.pop('password')
            return data

        errors = dict()
        try:
            validate_password(password=password, user=user)
        except django_core_exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise rest_serializers.ValidationError(errors)

        return data


class AvatarUploadSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = api_models.User
        fields = ('avatar',)
