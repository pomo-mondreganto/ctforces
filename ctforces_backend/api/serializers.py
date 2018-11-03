from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_core_exceptions
from guardian.shortcuts import assign_perm
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
    old_password = rest_serializers.CharField(write_only=True)

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
            'old_password',
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

        if password:
            instance.set_password(password)

        return super(UserMainSerializer, self).update(instance, validated_data)


class AvatarUploadSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = api_models.User
        fields = ('avatar',)


class TaskTagSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = api_models.TaskTag
        fields = ('id', 'name')


class TaskPreviewSerializer(rest_serializers.ModelSerializer):
    solved_count = rest_serializers.IntegerField(read_only=True)
    task_tags_details = TaskTagSerializer(many=True, read_only=True, source='tags')

    class Meta:
        model = api_models.Task
        fields = (
            'id',
            'name',
            'task_tags_details',
            'author',
            'cost',
            'publication_time',
            'solved_count',
        )


class TaskViewSerializer(rest_serializers.ModelSerializer):
    solved_count = rest_serializers.IntegerField(read_only=True)
    task_tags_details = TaskTagSerializer(many=True, read_only=True, source='tags')
    can_edit_task = rest_serializers.BooleanField(read_only=True)

    class Meta:
        model = api_models.Task
        fields = (
            'id',
            'name',
            'task_tags_details',
            'author',
            'cost',
            'publication_time',
            'description',
            'solved_count',
            'can_edit_task',
        )


class TaskFullSerializer(rest_serializers.ModelSerializer):
    solved_count = rest_serializers.IntegerField(read_only=True)
    task_tags_details = TaskTagSerializer(many=True, read_only=True, source='tags')

    class Meta:
        model = api_models.Task
        fields = (
            'id',
            'name',
            'task_tags_details',
            'tags',
            'author',
            'cost',
            'publication_time',
            'flag',
            'description',
            'is_published',
            'solved_count',
        )

        extra_kwargs = {
            'author': {
                'read_only': True,
            },
            'publication_time': {
                'read_only': True,
            },
        }

    def create(self, validated_data):
        instance = super(TaskFullSerializer, self).create(validated_data)
        instance.author = self.context['request'].user
        assign_perm('view_task', instance.author, instance)
        assign_perm('edit_task', instance.author, instance)
        assign_perm('delete_task', instance.author, instance)
        return instance


class TaskSubmitSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = api_models.Task
        fields = ('flag',)

    def validate_flag(self, flag):
        if flag != self.instance.flag:
            raise rest_serializers.ValidationError('Invalid flag.')


class TaskFileUploadSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = api_models.TaskFile
        fields = ('id', 'file_field', 'owner', 'name')
        extra_kwargs = {
            'owner': {
                'required': False,
            },
            'name': {
                'required': False,
            },
        }

    def __init__(self, *args, **kwargs):
        self.filename = None
        super(TaskFileUploadSerializer, self).__init__(*args, **kwargs)

    def validate_file_field(self, data):
        self.filename = data.name
        return data

    def validate(self, attrs):
        attrs['name'] = self.filename
        attrs['owner'] = self.context['request'].user
        return attrs


class TaskFileBasicSerializer(rest_serializers.ModelSerializer):
    task_details = TaskPreviewSerializer(read_only=True, source='task')

    class Meta:
        model = api_models.TaskFile
        fields = (
            'id',
            'name',
            'task_details',
            'upload_time'
        )
