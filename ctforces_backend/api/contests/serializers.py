from django.db import transaction
from django.db.utils import IntegrityError
from guardian.shortcuts import assign_perm
from rest_framework import serializers as rest_serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from api import fields as api_fields
from api import mixins as api_mixins
from api import models as api_models
from api.tasks import serializers as api_tasks_serializers
from api.teams import serializers as api_teams_serializers
from api.users import serializers as api_users_serializers


class CPRSerializer(rest_serializers.ModelSerializer):
    participant = api_fields.CurrentUserPermissionsFilteredPKRF(
        read_only=False,
        write_only=False,
        queryset=api_models.Team.objects.all(),
        perms='register_team',
    )

    registered_users_details = api_users_serializers.UserMinimalSerializer(
        many=True,
        read_only=True,
        source='registered_users',
    )

    rating = rest_serializers.IntegerField(read_only=True)

    participant_details = api_teams_serializers.TeamMinimalSerializer(
        read_only=True,
        source='participant',
    )

    class Meta:
        model = api_models.ContestParticipantRelationship
        fields = (
            'id',
            'contest',
            'participant',
            'rating',
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
                queryset=api_models.ContestParticipantRelationship.objects.all(),
                fields=['contest', 'participant'],
                message='Team is already registered',
            ),
        ]

    def validate_contest(self, contest):
        if not contest.is_published or not contest.is_registration_open:
            raise ValidationError("Contest doesn't exist or registration isn't open yet")

        if self.context['request'].user.has_perm('api.change_contest', contest):
            raise ValidationError('You cannot register for this contest')
        return contest

    def validate(self, attrs):
        team = attrs['participant']
        members = team.participants.only('id')
        diff = set(attrs['registered_users']).difference(set(members))
        if diff:
            raise ValidationError({'registered_users': f'You can\'t register users {diff}'})
        return attrs

    def update(self, instance, validated_data):
        validated_data.pop('contest', None)
        current_registrations = set(instance.registered_users.values_list('id', flat=True))
        new_registrations = set(map(lambda x: x.id, validated_data['registered_users']))
        to_delete = current_registrations.difference(new_registrations)
        to_create = new_registrations.difference(current_registrations)
        to_create_helpers = list(
            api_models.CPRHelper(contest=instance.contest, user_id=user_id, cpr=instance)
            for user_id in to_create
        )

        try:
            with transaction.atomic():
                api_models.CPRHelper.objects.bulk_create(to_create_helpers)
                api_models.CPRHelper.objects.filter(contest=instance.contest, user__id__in=to_delete).delete()
                new_instance = super(CPRSerializer, self).update(instance, validated_data)
        except IntegrityError:
            raise ValidationError({'detail': "User is already registered in another team"})

        return new_instance

    def create(self, validated_data):
        new_registrations = set(map(lambda x: x.id, validated_data['registered_users']))

        try:
            with transaction.atomic():
                instance = super(CPRSerializer, self).create(validated_data)
                to_create_helpers = list(
                    api_models.CPRHelper(
                        contest=validated_data['contest'],
                        user_id=user_id,
                        cpr=instance,
                    )
                    for user_id in new_registrations
                )
                api_models.CPRHelper.objects.bulk_create(to_create_helpers)
        except IntegrityError:
            raise ValidationError({'detail': "User is already registered in another team"})

        return instance


class CTRMainSerializer(rest_serializers.ModelSerializer):
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
            'max_cost',
            'min_cost',
            'decay_value',
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


class CTRUpdateSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = api_models.ContestTaskRelationship
        fields = (
            'cost',
            'id',
            'main_tag',
            'max_cost',
            'min_cost',
            'decay_value',
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

    class Meta:
        model = api_models.Task
        fields = (
            'id',
            'author_username',
            'can_edit_task',
            'contest_cost',
            'description',
            'files_details',
            'hints',
            'is_solved_by_user',
            'name',
            'ordering_number',
            'solved_count',
            'tags_details',
        )

    @staticmethod
    def get_hints_method(obj):
        return api_models.TaskHint.objects.filter(is_published=True, task=obj).values_list('id', flat=True)


class ContestFullSerializer(rest_serializers.ModelSerializer):
    author_username = rest_serializers.SlugRelatedField(read_only=True, slug_field='username', source='author')
    registered_count = rest_serializers.IntegerField(read_only=True)
    contest_task_relationship_details = CTRMainSerializer(
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
            'dynamic_scoring',
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
            'dynamic_scoring',
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
    contest_task_relationship_details = CTRMainSerializer(
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
            'dynamic_scoring',
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


class ContestScoreboardParticipantSerializer(rest_serializers.ModelSerializer, api_mixins.ReadOnlySerializerMixin):
    cost_sum = rest_serializers.IntegerField()
    last_contest_solve = rest_serializers.DateTimeField()
    registered_users = api_users_serializers.UserMinimalSerializer(
        many=True,
        read_only=True,
    )
    rating = rest_serializers.IntegerField(read_only=True)

    class Meta:
        model = api_models.Team
        fields = (
            'cost_sum',
            'id',
            'last_contest_solve',
            'name',
            'registered_users',
            'rating',
        )


class ContestScoreboardParticipantMinimalSerializer(rest_serializers.ModelSerializer,
                                                    api_mixins.ReadOnlySerializerMixin):
    class Meta:
        model = api_models.Team
        fields = (
            'id',
            'name',
        )
