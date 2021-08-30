from django.db import transaction
from django.db.utils import IntegrityError
from guardian.shortcuts import assign_perm
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

import api.fields
import api.models
from api.mixins import ReadOnlySerializerMixin
from api.tasks.serializers import TaskTagSerializer, TaskFileSerializer, TaskPreviewSerializer
from api.teams.serializers import TeamMinimalSerializer
from api.users.serializers import UserMinimalSerializer


class CPRSerializer(serializers.ModelSerializer):
    registered_users_details = UserMinimalSerializer(
        many=True,
        read_only=True,
        source='registered_users',
    )
    participant_details = TeamMinimalSerializer(
        read_only=True,
        source='participant',
    )

    class Meta:
        model = api.models.ContestParticipantRelationship
        fields = (
            'id',
            'contest',
            'participant',
            'participant_details',
            'registered_users',
            'registered_users_details',
        )
        extra_kwargs = {
            'registered_users': {
                'write_only': True,
            },
        }
        validators = [
            UniqueTogetherValidator(
                queryset=api.models.ContestParticipantRelationship.objects.all(),
                fields=['contest', 'participant'],
                message='Team is already registered',
            ),
        ]

    @staticmethod
    def validate_registered_users(data):
        if not data:
            raise ValidationError('Need to register at least one team member')
        return data

    def validate_contest(self, contest):
        if not contest.is_published or not contest.is_registration_open:
            raise ValidationError("Contest doesn't exist or registration isn't open yet")
        if self.context['request'].user.has_perm('api.change_contest', contest):
            raise ValidationError('You cannot register for this contest')
        return contest

    def validate_participant(self, participant):
        user = self.context['request'].user
        if not user.has_perm('api.register_team', participant):
            raise ValidationError('You cannot register this team for a contest.')
        return participant

    def validate(self, attrs):
        team = attrs['participant']
        registered_users = attrs['registered_users']
        members = team.participants.only('id')
        diff = set(registered_users) - set(members)
        if diff:
            raise ValidationError({'registered_users': f'You can\'t register users {diff}'})

        return attrs

    def create(self, validated_data):
        new_registrations = set(map(lambda x: x.id, validated_data['registered_users']))

        try:
            with transaction.atomic():
                instance = super(CPRSerializer, self).create(validated_data)
                to_create_helpers = list(
                    api.models.CPRHelper(
                        contest=validated_data['contest'],
                        user_id=user_id,
                        cpr=instance,
                    )
                    for user_id in new_registrations
                )
                api.models.CPRHelper.objects.bulk_create(to_create_helpers)
        except IntegrityError:
            raise ValidationError({'detail': "User is already registered in another team"})

        return instance

    def update(self, instance, validated_data):
        validated_data.pop('contest', None)
        current_registrations = set(instance.registered_users.values_list('id', flat=True))
        new_registrations = set(map(lambda x: x.id, validated_data['registered_users']))
        to_delete = current_registrations.difference(new_registrations)
        to_create = new_registrations.difference(current_registrations)
        to_create_helpers = list(
            api.models.CPRHelper(contest=instance.contest, user_id=user_id, cpr=instance)
            for user_id in to_create
        )

        try:
            with transaction.atomic():
                api.models.CPRHelper.objects.bulk_create(to_create_helpers)
                api.models.CPRHelper.objects.filter(contest=instance.contest, user__id__in=to_delete).delete()
                new_instance = super(CPRSerializer, self).update(instance, validated_data)
        except IntegrityError:
            raise ValidationError({'detail': "User is already registered in another team"})

        return new_instance


class CTRSerializer(serializers.ModelSerializer):
    solved_count = serializers.IntegerField(read_only=True)
    is_solved_by_user = serializers.BooleanField(read_only=True)

    main_tag_details = TaskTagSerializer(
        read_only=True,
        source='main_tag',
    )
    task_details = TaskPreviewSerializer(read_only=True, source='task')

    class Meta:
        model = api.models.ContestTaskRelationship
        fields = (
            'contest',
            'cost',
            'id',
            'is_solved_by_user',
            'main_tag',
            'main_tag_details',
            'min_cost',
            'decay_value',
            'solved_count',
            'task',
            'task_details',
        )

    def validate_contest(self, contest):
        user = self.context['request'].user
        if not user.has_perm('api.change_contest', contest):
            raise ValidationError('You cannot change this contest.')
        return contest

    def validate_task(self, task):
        user = self.context['request'].user
        if not user.has_perm('api.change_task', task):
            raise ValidationError('You cannot change this task.')
        return task


class ContestTaskPreviewSerializer(serializers.ModelSerializer, ReadOnlySerializerMixin):
    solved_count = serializers.IntegerField(read_only=True)
    tags_details = TaskTagSerializer(many=True, read_only=True, source='tags')
    contest_cost = serializers.IntegerField(read_only=True)
    is_solved_by_user = serializers.BooleanField(read_only=True)
    is_solved_on_upsolving = serializers.BooleanField(read_only=True)
    author_username = serializers.SlugRelatedField(read_only=True, slug_field='username', source='author')
    main_tag_details = TaskTagSerializer(read_only=True, source='main_tag')

    class Meta:
        model = api.models.Task
        fields = (
            'id',
            'author_username',
            'contest_cost',
            'is_solved_by_user',
            'is_solved_on_upsolving',
            'name',
            'solved_count',
            'tags_details',
            'main_tag_details',
        )


class ContestTaskViewSerializer(serializers.ModelSerializer, ReadOnlySerializerMixin):
    solved_count = serializers.IntegerField(read_only=True)
    tags_details = TaskTagSerializer(many=True, read_only=True, source='tags')
    files_details = TaskFileSerializer(many=True, read_only=True, source='files')
    can_edit_task = serializers.BooleanField(read_only=True)
    is_solved_by_user = serializers.BooleanField(read_only=True)
    is_solved_on_upsolving = serializers.BooleanField(read_only=True)
    author_username = serializers.SlugRelatedField(read_only=True, slug_field='username', source='author')
    hints = serializers.SerializerMethodField('get_hints_method')
    contest_cost = serializers.IntegerField(read_only=True)

    class Meta:
        model = api.models.Task
        fields = (
            'id',
            'author_username',
            'can_edit_task',
            'contest_cost',
            'description',
            'files_details',
            'hints',
            'is_solved_by_user',
            'is_solved_on_upsolving',
            'name',
            'solved_count',
            'tags_details',
        )

    @staticmethod
    def get_hints_method(obj):
        return obj.hints.filter(is_published=True).values_list('id', flat=True)


class ContestFullSerializer(serializers.ModelSerializer):
    author_username = serializers.SlugRelatedField(read_only=True, slug_field='username', source='author')
    registered_count = serializers.IntegerField(read_only=True)
    contest_task_relationship_details = CTRSerializer(
        many=True,
        read_only=True,
        source='contest_task_relationship',
    )

    class Meta:
        model = api.models.Contest
        fields = (
            'author',
            'author_username',
            'always_recalculate_rating',
            'contest_task_relationship_details',
            'created_at',
            'description',
            'dynamic_scoring',
            'end_time',
            'id',
            'is_finished',
            'is_published',
            'is_rated',
            'is_registration_open',
            'is_running',
            'is_virtual',
            'virtual_duration',
            'name',
            'public_scoreboard',
            'publish_tasks_after_finished',
            'randomize_tasks',
            'randomize_tasks_count',
            'registered_count',
            'start_time',
            'updated_at',
        )

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        instance = super(ContestFullSerializer, self).create(validated_data)
        assign_perm('view_contest', instance.author, instance)
        assign_perm('change_contest', instance.author, instance)
        assign_perm('delete_contest', instance.author, instance)
        return instance


class ContestPreviewSerializer(serializers.ModelSerializer, ReadOnlySerializerMixin):
    registered_count = serializers.IntegerField(read_only=True)
    author_username = serializers.SlugRelatedField(read_only=True, slug_field='username', source='author')
    is_registered = serializers.BooleanField(read_only=True)
    opened_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = api.models.Contest
        fields = (
            'author_username',
            'dynamic_scoring',
            'end_time',
            'id',
            'is_finished',
            'is_published',
            'is_rated',
            'is_registered',
            'is_registration_open',
            'is_running',
            'is_virtual',
            'virtual_duration',
            'name',
            'registered_count',
            'start_time',
            'opened_at',
        )


class ContestViewSerializer(serializers.ModelSerializer, ReadOnlySerializerMixin):
    can_edit_contest = serializers.BooleanField(read_only=True)
    can_view_scoreboard = serializers.BooleanField(read_only=True)
    opened_at = serializers.DateTimeField(read_only=True)
    author_username = serializers.SlugRelatedField(read_only=True, slug_field='username', source='author')

    class Meta:
        model = api.models.Contest
        fields = (
            'author_username',
            'can_edit_contest',
            'can_view_scoreboard',
            'created_at',
            'description',
            'dynamic_scoring',
            'end_time',
            'id',
            'is_finished',
            'is_published',
            'is_rated',
            'is_registration_open',
            'is_running',
            'is_virtual',
            'virtual_duration',
            'name',
            'start_time',
            'opened_at',
            'updated_at',
        )


class ContestScoreboardParticipantSerializer(serializers.ModelSerializer, ReadOnlySerializerMixin):
    cost_sum = serializers.IntegerField()
    last_contest_solve = serializers.DateTimeField()
    registered_users = UserMinimalSerializer(
        many=True,
        read_only=True,
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = api.models.Team
        fields = (
            'cost_sum',
            'id',
            'last_contest_solve',
            'name',
            'registered_users',
            'rating',
        )
