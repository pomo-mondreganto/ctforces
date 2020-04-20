from guardian.shortcuts import assign_perm, remove_perm
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
            'id',
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
            'id',
            'name',
            'join_token',
            'created_at',
            'captain_details',
            'captain',
            'participants_details',
            'can_edit_team',
            'can_delete_team',
        )

    def validate_captain(self, captain):
        if self.instance and captain:
            if isinstance(captain, int):
                exists = self.instance.participants.filter(id=captain)
            else:
                exists = self.instance.participants.filter(id=captain.id)

            if not exists:
                raise rest_serializers.ValidationError('Only a team member can be made captain')
        return captain

    def update(self, instance, validated_data):
        if 'join_token' in validated_data:
            name = validated_data.get('name', instance.name)
            validated_data['join_token'] = api_models.Team.gen_join_token(name)
        if 'captain' in validated_data and validated_data['captain'] != instance.captain:
            new_captain = validated_data['captain']
            assign_perm('view_team', new_captain, instance)
            assign_perm('change_team', new_captain, instance)
            assign_perm('delete_team', new_captain, instance)

            remove_perm('view_team', instance.captain, instance)
            remove_perm('change_team', instance.captain, instance)
            remove_perm('delete_team', instance.captain, instance)

        return super(TeamFullSerializer, self).update(instance, validated_data)

    def create(self, validated_data):
        validated_data['captain'] = self.context['request'].user
        validated_data['join_token'] = api_models.Team.gen_join_token(validated_data["name"])
        instance = super(TeamFullSerializer, self).create(validated_data)
        assign_perm('view_team', instance.captain, instance)
        assign_perm('change_team', instance.captain, instance)
        assign_perm('delete_team', instance.captain, instance)
        assign_perm('register_team', instance.captain, instance)
        instance.participants.add(instance.captain)
        return instance


class TeamContestsHistorySerializer(rest_serializers.ModelSerializer, ReadOnlySerializerMixin):
    contest_title = rest_serializers.SlugRelatedField(
        read_only=True,
        slug_field='title',
        source='contest',
    )
    registered_users_details = api_users_serializers.UserMinimalSerializer(
        many=True,
        read_only=True,
        source='registered_users',
    )

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
