from guardian.shortcuts import assign_perm
from rest_framework import serializers as rest_serializers

from api import fields as api_fields
from api import mixins as api_mixins
from api import models as api_models
from api.tasks import serializers as api_tasks_serializers


class ContestTaskRelationshipMainSerializer(rest_serializers.ModelSerializer):
    solved_count = rest_serializers.IntegerField(read_only=True)
    is_solved_by_user = rest_serializers.BooleanField(read_only=True)
    task_name = rest_serializers.SlugRelatedField(read_only=True, slug_field='name', source='task')

    main_tag_details = api_tasks_serializers.TaskTagSerializer(
        read_only=True,
        source='main_tag',
    )

    contest = api_fields.CurrentUserPermissionsFilteredPKRF(
        read_only=False,
        write_only=True,
        queryset=api_models.Contest.objects.all(),
        perms='change_contest',
    )

    task = api_fields.CurrentUserPermissionsFilteredPKRF(
        read_only=False,
        queryset=api_models.Task.objects.all(),
        perms='change_task',
        additional_queryset=api_models.Task.objects.filter(is_published=True),
    )

    class Meta:
        model = api_models.ContestTaskRelationship
        fields = (
            'contest',
            'cost',
            'id',
            'is_solved_by_user',
            'main_tag',
            'main_tag_details',
            'ordering_number',
            'solved_count',
            'task',
            'task_name',
        )

        extra_kwargs = {
            'main_tag': {
                'write_only': True,
            },
        }


class ContestTaskRelationshipUpdateSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = api_models.ContestTaskRelationship
        fields = (
            'cost',
            'id',
            'main_tag',
            'ordering_number',
        )


class ContestTaskPreviewSerializer(rest_serializers.ModelSerializer, api_mixins.ReadOnlySerializerMixin):
    solved_count = rest_serializers.IntegerField(read_only=True)
    tags_details = api_tasks_serializers.TaskTagSerializer(many=True, read_only=True, source='tags')
    contest_cost = rest_serializers.IntegerField(read_only=True)
    is_solved_by_user = rest_serializers.BooleanField(read_only=True)
    author_username = rest_serializers.SlugRelatedField(read_only=True, slug_field='username', source='author')
    ordering_number = rest_serializers.IntegerField(read_only=True)

    class Meta:
        model = api_models.Task
        fields = (
            'author_username',
            'contest_cost',
            'is_solved_by_user',
            'name',
            'ordering_number',
            'solved_count',
            'tags_details',
        )


class ContestTaskViewSerializer(rest_serializers.ModelSerializer, api_mixins.ReadOnlySerializerMixin):
    solved_count = rest_serializers.IntegerField(read_only=True)
    tags_details = api_tasks_serializers.TaskTagSerializer(many=True, read_only=True, source='tags')
    files_details = api_tasks_serializers.TaskFileViewSerializer(many=True, read_only=True, source='files')
    can_edit_task = rest_serializers.BooleanField(read_only=True)
    is_solved_by_user = rest_serializers.BooleanField(read_only=True)
    author_username = rest_serializers.SlugRelatedField(read_only=True, slug_field='username', source='author')
    hints = rest_serializers.SerializerMethodField('get_hints_method')
    contest_cost = rest_serializers.IntegerField(read_only=True)
    ordering_number = rest_serializers.IntegerField(read_only=True)
    real_id = rest_serializers.IntegerField(read_only=True)

    class Meta:
        model = api_models.Task
        fields = (
            'author_username',
            'can_edit_task',
            'contest_cost',
            'description',
            'files_details',
            'hints',
            'is_solved_by_user',
            'name',
            'ordering_number',
            'real_id',
            'solved_count',
            'tags_details',
        )

    @staticmethod
    def get_hints_method(obj):
        return api_models.TaskHint.objects.filter(is_published=True, task=obj).values_list('id', flat=True)


class ContestFullSerializer(rest_serializers.ModelSerializer):
    author_username = rest_serializers.SlugRelatedField(read_only=True, slug_field='username', source='author')
    registered_count = rest_serializers.IntegerField(read_only=True)
    contest_task_relationship_details = ContestTaskRelationshipMainSerializer(
        many=True,
        read_only=True,
        source='contest_task_relationship',
    )

    class Meta:
        model = api_models.Contest
        fields = (
            'author',
            'author_username',
            'contest_task_relationship_details',
            'created_at',
            'description',
            'end_time',
            'id',
            'is_finished',
            'is_published',
            'is_rated',
            'is_registration_open',
            'is_running',
            'name',
            'publish_tasks_after_finished',
            'registered_count',
            'start_time',
            'updated_at',
        )

        extra_kwargs = {
            'author': {
                'write_only': True,
            },
        }

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        instance = super(ContestFullSerializer, self).create(validated_data)
        assign_perm('view_contest', instance.author, instance)
        assign_perm('change_contest', instance.author, instance)
        assign_perm('delete_contest', instance.author, instance)
        return instance


class ContestPreviewSerializer(rest_serializers.ModelSerializer, api_mixins.ReadOnlySerializerMixin):
    registered_count = rest_serializers.IntegerField(read_only=True)
    author_username = rest_serializers.SlugRelatedField(read_only=True, slug_field='username', source='author')
    is_registered = rest_serializers.BooleanField(read_only=True)

    class Meta:
        model = api_models.Contest
        fields = (
            'author_username',
            'end_time',
            'id',
            'is_finished',
            'is_published',
            'is_rated',
            'is_registered',
            'is_registration_open',
            'is_running',
            'name',
            'registered_count',
            'start_time',
        )


class ContestViewSerializer(rest_serializers.ModelSerializer, api_mixins.ReadOnlySerializerMixin):
    can_edit_contest = rest_serializers.BooleanField(read_only=True)
    author_username = rest_serializers.SlugRelatedField(read_only=True, slug_field='username', source='author')
    contest_task_relationship_details = ContestTaskRelationshipMainSerializer(
        many=True,
        read_only=True,
        source='contest_task_relationship',
    )

    class Meta:
        model = api_models.Contest
        fields = (
            'author',
            'author_username',
            'can_edit_contest',
            'contest_task_relationship_details',
            'created_at',
            'end_time',
            'id',
            'is_finished',
            'is_published',
            'is_rated',
            'is_registration_open',
            'is_running',
            'name',
            'start_time',
            'updated_at',
        )

        extra_kwargs = {
            'author': {
                'write_only': True,
            },
        }


class ContestScoreboardUserSerializer(rest_serializers.ModelSerializer, api_mixins.ReadOnlySerializerMixin):
    cost_sum = rest_serializers.IntegerField()
    last_contest_solve = rest_serializers.DateTimeField()

    class Meta:
        model = api_models.User
        fields = (
            'cost_sum',
            'id',
            'last_contest_solve',
            'username',
        )


class ContestScoreboardUserMinimalSerializer(rest_serializers.ModelSerializer, api_mixins.ReadOnlySerializerMixin):
    class Meta:
        model = api_models.User
        fields = (
            'id',
            'username',
        )


class ContestScoreboardSerializer(rest_serializers.ModelSerializer, api_mixins.ReadOnlySerializerMixin):
    task_name = rest_serializers.CharField()

    class Meta:
        model = api_models.ContestTaskParticipantSolvedRelationship
        fields = (
            'participant_id',
            'task_name',
        )
