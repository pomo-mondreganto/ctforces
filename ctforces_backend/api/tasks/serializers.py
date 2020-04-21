from guardian.shortcuts import assign_perm
from rest_framework import serializers as rest_serializers
from rest_framework.exceptions import ValidationError

from api import fields as api_fields
from api import mixins as api_mixins
from api import models as api_models


class TaskTagSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = api_models.TaskTag
        fields = ('id', 'name')
        extra_kwargs = {
            'name': {
                'required': True,
                'validators': [],
            },
        }

    @staticmethod
    def validate_name(data):
        return data.lower()

    def create(self, validated_data):
        instance, _ = api_models.TaskTag.objects.get_or_create(**validated_data)
        return instance


class TaskPreviewSerializer(rest_serializers.ModelSerializer, api_mixins.ReadOnlySerializerMixin):
    solved_count = rest_serializers.IntegerField(read_only=True)
    task_tags_details = TaskTagSerializer(many=True, read_only=True, source='tags')
    is_solved_by_user = rest_serializers.BooleanField(read_only=True)

    class Meta:
        model = api_models.Task
        fields = (
            'author',
            'cost',
            'id',
            'is_published',
            'is_solved_by_user',
            'name',
            'publication_time',
            'solved_count',
            'task_tags_details',
        )


class TaskFileMainSerializer(rest_serializers.ModelSerializer):
    task_details = TaskPreviewSerializer(read_only=True, source='task')

    class Meta:
        model = api_models.TaskFile
        fields = (
            'file_field',
            'id',
            'name',
            'owner',
            'task_details',
            'upload_time',
        )
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
        super(TaskFileMainSerializer, self).__init__(*args, **kwargs)

    def validate_file_field(self, data):
        self.filename = data.name
        return data

    def validate_owner(self, data):
        if self.instance and data != self.instance.owner:
            raise ValidationError({'owner': 'This field is immutable once set'})
        return data

    def validate(self, attrs):
        attrs['name'] = self.filename
        return attrs

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        instance = super(TaskFileMainSerializer, self).create(validated_data)
        assign_perm('view_taskfile', instance.owner, instance)
        assign_perm('change_taskfile', instance.owner, instance)
        assign_perm('delete_taskfile', instance.owner, instance)
        return instance


class TaskFileViewSerializer(rest_serializers.ModelSerializer, api_mixins.ReadOnlySerializerMixin):
    class Meta:
        model = api_models.TaskFile
        fields = (
            'file_field',
            'id',
            'name',
            'upload_time',
        )

        extra_kwargs = {
            'file_field': {
                'use_url': False,
            },
        }


class TaskViewSerializer(rest_serializers.ModelSerializer, api_mixins.ReadOnlySerializerMixin):
    solved_count = rest_serializers.IntegerField(read_only=True)
    tags_details = TaskTagSerializer(many=True, read_only=True, source='tags')
    files_details = TaskFileViewSerializer(many=True, read_only=True, source='files')
    can_edit_task = rest_serializers.BooleanField(read_only=True)
    is_solved_by_user = rest_serializers.BooleanField(read_only=True)
    author_username = rest_serializers.SlugRelatedField(read_only=True, slug_field='username', source='author')
    author_rating = rest_serializers.SlugRelatedField(read_only=True, slug_field='rating', source='author')
    hints = rest_serializers.SerializerMethodField('get_hints_method')

    class Meta:
        model = api_models.Task
        fields = (
            'author_rating',
            'author_username',
            'can_edit_task',
            'cost',
            'description',
            'files_details',
            'hints',
            'id',
            'is_published',
            'is_solved_by_user',
            'name',
            'publication_time',
            'solved_count',
            'tags_details',
        )

    @staticmethod
    def get_hints_method(obj):
        return api_models.TaskHint.objects.filter(is_published=True, task=obj).values_list('id', flat=True)


class TaskFullSerializer(rest_serializers.ModelSerializer):
    solved_count = rest_serializers.IntegerField(read_only=True)
    task_tags_details = TaskTagSerializer(many=True, read_only=True, source='tags')
    files_details = TaskFileViewSerializer(many=True, read_only=True, source='files')
    cost = rest_serializers.IntegerField(min_value=1, max_value=9999)
    author_username = rest_serializers.SlugRelatedField(read_only=True, slug_field='username', source='author')
    author_rating = rest_serializers.SlugRelatedField(read_only=True, slug_field='rating', source='author')
    files = api_fields.CurrentUserPermissionsFilteredPKRF(
        read_only=False,
        write_only=True,
        queryset=api_models.TaskFile.objects.all(),
        perms='view_taskfile',
        many=True,
    )

    class Meta:
        model = api_models.Task
        fields = (
            'author',
            'author_rating',
            'author_username',
            'cost',
            'description',
            'files',
            'files_details',
            'flag',
            'hints',
            'id',
            'is_published',
            'name',
            'publication_time',
            'solved_count',
            'tags',
            'task_tags_details',
        )

        extra_kwargs = {
            'author': {
                'write_only': True,
            },
            'publication_time': {
                'read_only': True,
            },
            'tags': {
                'write_only': True,
            },
        }

    @staticmethod
    def validate_tags(data):
        if len(data) < 1:
            raise rest_serializers.ValidationError('Please specify at least one tag')
        if len(data) > 5:
            raise rest_serializers.ValidationError('You are allowed to use 5 tags or less.')
        return data

    @staticmethod
    def validate_files(data):
        if len(data) > 5:
            raise rest_serializers.ValidationError('You are allowed to include 5 files or less.')
        return data

    def validate_owner(self, data):
        if self.instance and data != self.instance.owner:
            raise ValidationError({'owner': 'This field is immutable once set'})
        return data

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        instance = super(TaskFullSerializer, self).create(validated_data)
        assign_perm('view_task', instance.author, instance)
        assign_perm('change_task', instance.author, instance)
        assign_perm('delete_task', instance.author, instance)
        return instance

    def update(self, instance, validated_data):
        if 'is_published' in validated_data and not validated_data['is_published']:
            validated_data['show_on_main_page'] = False
        return super(TaskFullSerializer, self).update(instance, validated_data)


class TaskSubmitSerializer(rest_serializers.ModelSerializer, api_mixins.ReadOnlySerializerMixin):
    class Meta:
        model = api_models.Task
        fields = ('flag',)

    def validate_flag(self, flag):
        if flag != self.instance.flag:
            raise rest_serializers.ValidationError('Invalid flag.')


class TaskHintSerializer(rest_serializers.ModelSerializer):
    task = api_fields.CurrentUserPermissionsFilteredPKRF(
        read_only=False,
        perms='change_task',
        queryset=api_models.Task.objects.all(),
    )

    author_username = rest_serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        source='author',
    )

    author_rating = rest_serializers.SlugRelatedField(
        read_only=True,
        slug_field='rating',
        source='author',
    )

    class Meta:
        model = api_models.TaskHint
        fields = (
            'author',
            'author_rating',
            'author_username',
            'body',
            'is_published',
            'task',
        )

        extra_kwargs = {
            'author': {
                'write_only': True,
            },
            'task': {
                'write_only': True,
            }
        }

    def validate_author(self, data):
        if self.instance and data != self.instance.author:
            raise ValidationError({'author': 'This field is immutable once set'})
        return data

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        instance = super(TaskHintSerializer, self).create(validated_data)
        assign_perm('view_taskhint', instance.author, instance)
        assign_perm('change_taskhint', instance.author, instance)
        assign_perm('delete_taskhint', instance.author, instance)
        return instance
