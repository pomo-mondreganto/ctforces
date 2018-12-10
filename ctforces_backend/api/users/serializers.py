from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_core_exceptions
from guardian.shortcuts import assign_perm
from rest_framework import serializers as rest_serializers
from rest_framework.fields import empty

from api import models as api_models


class UserCreateSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = api_models.User
        fields = (
            'id',
            'email',
            'password',
            'username',
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
        assign_perm('view_personal_info', user, user)
        return user


class UserPersonalInfoSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = api_models.User
        fields = (
            'first_name',
            'last_name',
        )
        nested_proxy_field = True


class UserBasicSerializer(rest_serializers.ModelSerializer):
    avatar_main = rest_serializers.URLField(source='avatar.main.url')
    avatar_small = rest_serializers.URLField(source='avatar.small.url')
    cost_sum = rest_serializers.IntegerField(read_only=True)
    personal_info = UserPersonalInfoSerializer(read_only=True)

    class Meta:
        model = api_models.User
        fields = (
            'id',
            'avatar_main',
            'avatar_small',
            'cost_sum',
            'hide_personal_info',
            'max_rating',
            'personal_info',
            'rating',
            'username',
        )

    def __init__(self, instance=None, data=empty, **kwargs):
        super(UserBasicSerializer, self).__init__(instance=instance, data=data, **kwargs)
        if isinstance(instance, list) \
                or (instance.hide_personal_info
                    and not self.context['request'].user.has_perm('view_personal_info', instance)):
            self.fields.pop('personal_info')


class UserMainSerializer(rest_serializers.ModelSerializer):
    cost_sum = rest_serializers.IntegerField(read_only=True)
    avatar_main = rest_serializers.URLField(source='avatar.main.url', read_only=True)
    avatar_small = rest_serializers.URLField(source='avatar.small.url', read_only=True)
    old_password = rest_serializers.CharField(write_only=True, required=False)
    password = rest_serializers.CharField(write_only=True, required=False)
    personal_info = UserPersonalInfoSerializer(required=False)

    class Meta:
        model = api_models.User
        fields = (
            'id',
            'avatar_main',
            'avatar_small',
            'cost_sum',
            'email',
            'hide_personal_info',
            'max_rating',
            'old_password',
            'password',
            'personal_info',
            'rating',
            'username',
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
        password = data.pop('password', None)
        old_password = data.pop('old_password', None)

        user = self.instance

        if not password:
            return data

        if not old_password:
            raise rest_serializers.ValidationError(
                {
                    'old_password': 'To change password you need to provide the old one.'
                }
            )
        if not user.check_password(raw_password=old_password):
            raise rest_serializers.ValidationError(
                {
                    'old_password': 'Old password is incorrect.'
                }
            )

        errors = dict()
        try:
            validate_password(password=password, user=user)
        except django_core_exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise rest_serializers.ValidationError(errors)

        data['password'] = password
        return data

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        personal_info = validated_data.pop('personal_info', None)
        if personal_info:
            validated_data.update(**personal_info)

        if password:
            instance.set_password(password)

        return super(UserMainSerializer, self).update(instance, validated_data)


class AvatarUploadSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = api_models.User
        fields = ('avatar',)
