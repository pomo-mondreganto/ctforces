from guardian.shortcuts import assign_perm
from rest_framework import serializers as rest_serializers

from api import models as api_models


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


class TaskFullSerializer(rest_serializers.ModelSerializer):
    solved_count = rest_serializers.IntegerField(read_only=True)
    task_tags_details = TaskTagSerializer(many=True, read_only=True, source='tags')
    files_details = TaskFileBasicSerializer(many=True, read_only=True, source='files')

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
            'files',
            'files_details',
        )

        extra_kwargs = {
            'author': {
                'read_only': True,
            },
            'publication_time': {
                'read_only': True,
            },
            'tags': {
                'read_only': True,
            },
            'files': {
                'read_only': True,
            },
        }

    @staticmethod
    def validate_tags(data):
        cur_tags = set()
        for tag in data:
            if tag.id not in cur_tags:
                cur_tags.add(tag.id)
            if len(cur_tags) > 5:
                raise rest_serializers.ValidationError('You are allowed to use 5 tags or less.')
        return data

    def validate(self, attrs):
        attrs['author'] = self.context['request'].user
        return attrs

    def create(self, validated_data):
        instance = super(TaskFullSerializer, self).create(validated_data)
        assign_perm('view_task', instance.author, instance)
        assign_perm('change_task', instance.author, instance)
        assign_perm('delete_task', instance.author, instance)
        return instance


class TaskSubmitSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = api_models.Task
        fields = ('flag',)

    def validate_flag(self, flag):
        if flag != self.instance.flag:
            raise rest_serializers.ValidationError('Invalid flag.')
