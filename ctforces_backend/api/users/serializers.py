from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_core_exceptions
from guardian.shortcuts import assign_perm
from rest_framework import serializers as rest_serializers
from rest_framework import validators as rest_validators
from rest_framework.fields import empty

from api import mixins as api_mixins
from api import models as api_models


class UserCreateSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = api_models.User
        fields = (
            'email',
            'id',
            'password',
            'username',
        )
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'username': {
                'validators': [
                    api_models.User.username_validator,
                    rest_validators.UniqueValidator(
                        queryset=api_models.User.objects.all(),
                        message='User with this username already exists',
                    ),
                ],
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


class UserPasswordResetSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = api_models.User
        fields = (
            'password',
        )
        extra_kwargs = {
            'password': {
                'write_only': True,
            },
        }

    def validate(self, data):
        password = data.get('password')

        errors = dict()
        try:
            validate_password(password=password, user=self.instance)
        except django_core_exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise rest_serializers.ValidationError(errors)

        return data

    def update(self, instance, validated_data):
        password = validated_data.pop('password')
        instance.set_password(password)
        return super(UserPasswordResetSerializer, self).update(instance=instance, validated_data=validated_data)


class UserPersonalInfoSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = api_models.User
        fields = (
            'first_name',
            'last_name',
        )
        nested_proxy_field = True


class UserBasicSerializer(rest_serializers.ModelSerializer, api_mixins.ReadOnlySerializerMixin):
    avatar_main = rest_serializers.URLField(source='avatar.main.url')
    avatar_small = rest_serializers.URLField(source='avatar.small.url')
    cost_sum = rest_serializers.IntegerField(read_only=True)
    personal_info = UserPersonalInfoSerializer(read_only=True)

    class Meta:
        model = api_models.User
        fields = (
            'avatar_main',
            'avatar_small',
            'cost_sum',
            'has_participated_in_rated_contest',
            'hide_personal_info',
            'id',
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


class UserMinimalSerializer(rest_serializers.ModelSerializer, api_mixins.ReadOnlySerializerMixin):
    cost_sum = rest_serializers.IntegerField(read_only=True)

    class Meta:
        model = api_models.User
        fields = (
            'cost_sum',
            'id',
            'rating',
            'username',
        )


class UserMainSerializer(rest_serializers.ModelSerializer):
    cost_sum = rest_serializers.IntegerField(read_only=True)
    avatar_main = rest_serializers.URLField(source='avatar.main.url', read_only=True)
    avatar_small = rest_serializers.URLField(source='avatar.small.url', read_only=True)
    old_password = rest_serializers.CharField(write_only=True, required=False)
    password = rest_serializers.CharField(write_only=True, required=False)
    personal_info = UserPersonalInfoSerializer(required=False)
    can_create_tasks = rest_serializers.BooleanField(read_only=True)
    can_create_posts = rest_serializers.BooleanField(read_only=True)
    can_create_contests = rest_serializers.BooleanField(read_only=True)
    can_create_taskfiles = rest_serializers.BooleanField(read_only=True)
    has_tasks = rest_serializers.BooleanField(read_only=True)
    has_posts = rest_serializers.BooleanField(read_only=True)
    has_contests = rest_serializers.BooleanField(read_only=True)
    is_admin = rest_serializers.BooleanField(read_only=True)

    class Meta:
        model = api_models.User
        fields = (
            'avatar_main',
            'avatar_small',
            'can_create_contests',
            'can_create_posts',
            'can_create_taskfiles',
            'can_create_tasks',
            'cost_sum',
            'email',
            'has_contests',
            'has_posts',
            'has_tasks',
            'is_admin',
            'hide_personal_info',
            'id',
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
            'rating': {
                'read_only': True,
            },
            'max_rating': {
                'read_only': True,
            },
            'username': {
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
