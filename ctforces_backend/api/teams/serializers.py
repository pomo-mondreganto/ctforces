from rest_framework import serializers as rest_serializers

from api import models as api_models
from api.mixins import ReadOnlySerializerMixin
from api.users import serializers as api_users_serializers


class TeamMinimalSerializer(rest_serializers.ModelSerializer, ReadOnlySerializerMixin):
    rating = rest_serializers.IntegerField(read_only=True)

    class Meta:
        model = api_models.Team
        fields = (
            'id',
            'name',
            'rating',
        )


class TeamViewSerializer(rest_serializers.ModelSerializer, ReadOnlySerializerMixin):
    captain_details = api_users_serializers.UserMinimalSerializer(
        read_only=True,
        source='captain',
    )
    participants_details = api_users_serializers.UserMinimalSerializer(
        many=True,
        read_only=True,
        source='participants',
    )

    can_edit_team = rest_serializers.BooleanField(read_only=True)
    can_delete_team = rest_serializers.BooleanField(read_only=True)

    class Meta:
        model = api_models.Team
        fields = (
            'name',
            'created_at',
            'captain_details',
            'participants_details',
            'can_edit_team',
            'can_delete_team',
        )


class TeamFullSerializer(rest_serializers.ModelSerializer):
    captain_details = api_users_serializers.UserMinimalSerializer(
        read_only=True,
        source='captain',
    )
    participants_details = api_users_serializers.UserMinimalSerializer(
        many=True,
        read_only=True,
        source='participants',
    )

    can_edit_team = rest_serializers.BooleanField(read_only=True)
    can_delete_team = rest_serializers.BooleanField(read_only=True)

    class Meta:
        model = api_models.Team
        fields = (
            'name',
            'join_token',
            'created_at',
            'captain_details',
            'captain',
            'participants',
            'participants_details',
            'can_edit_team',
            'can_delete_team',
        )


class TeamContestsHistorySerializer(rest_serializers.ModelSerializer, ReadOnlySerializerMixin):
    contest_title = rest_serializers.SlugRelatedField(read_only=True, slug_field='title', source='contest')

    class Meta:
        model = api_models.ContestParticipantRelationship
        fields = (
            'id',
            'contest',
            'contest_title',
            'delta',
            'has_opened_contest',
            'registered_users_details',
        )
