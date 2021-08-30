from guardian.shortcuts import assign_perm, remove_perm
from rest_framework import serializers

import api.models
import api.users.serializers
from api.mixins import ReadOnlySerializerMixin


class TeamMinimalSerializer(serializers.ModelSerializer, ReadOnlySerializerMixin):
    class Meta:
        model = api.models.Team
        fields = (
            'id',
            'name',
            'rating',
        )


class TeamViewSerializer(serializers.ModelSerializer, ReadOnlySerializerMixin):
    captain_details = api.users.serializers.UserMinimalSerializer(
        read_only=True,
        source='captain',
    )
    participants_details = api.users.serializers.UserMinimalSerializer(
        many=True,
        read_only=True,
        source='participants',
    )

    can_edit_team = serializers.BooleanField(read_only=True)
    can_delete_team = serializers.BooleanField(read_only=True)

    class Meta:
        model = api.models.Team
        fields = (
            'id',
            'name',
            'created_at',
            'captain_details',
            'participants_details',
            'can_edit_team',
            'can_delete_team',
            'rating',
            'max_rating',
        )

        extra_kwargs = {
            'rating': {
                'read_only': True,
            },
            'max_rating': {
                'read_only': True,
            },
        }


class TeamFullSerializer(serializers.ModelSerializer):
    captain_details = api.users.serializers.UserMinimalSerializer(
        read_only=True,
        source='captain',
    )
    participants_details = api.users.serializers.UserMinimalSerializer(
        many=True,
        read_only=True,
        source='participants',
    )

    can_edit_team = serializers.BooleanField(read_only=True)
    can_delete_team = serializers.BooleanField(read_only=True)

    class Meta:
        model = api.models.Team
        fields = (
            'id',
            'name',
            'join_token',
            'created_at',
            'captain_details',
            'captain',
            'rating',
            'max_rating',
            'participants_details',
            'can_edit_team',
            'can_delete_team',
        )

        extra_kwargs = {
            'rating': {
                'read_only': True,
            },
            'max_rating': {
                'read_only': True,
            },
        }

    def validate_captain(self, captain):
        if self.instance and captain:
            if isinstance(captain, int):
                exists = self.instance.participants.filter(id=captain)
            else:
                exists = self.instance.participants.filter(id=captain.id)

            if not exists:
                raise serializers.ValidationError('Only a team member can be made captain')
        return captain

    def create(self, validated_data):
        validated_data['captain'] = self.context['request'].user
        validated_data['join_token'] = api.models.Team.gen_join_token(validated_data["name"])
        instance = super(TeamFullSerializer, self).create(validated_data)
        assign_perm('view_team', instance.captain, instance)
        assign_perm('change_team', instance.captain, instance)
        assign_perm('delete_team', instance.captain, instance)
        assign_perm('register_team', instance.captain, instance)
        instance.participants.add(instance.captain)
        return instance

    def update(self, instance, validated_data):
        if 'join_token' in validated_data or 'name' in validated_data:
            name = validated_data.get('name', instance.name)
            validated_data['join_token'] = api.models.Team.gen_join_token(name)
        if 'captain' in validated_data and validated_data['captain'] != instance.captain:
            new_captain = validated_data['captain']
            assign_perm('view_team', new_captain, instance)
            assign_perm('change_team', new_captain, instance)
            assign_perm('delete_team', new_captain, instance)

            remove_perm('view_team', instance.captain, instance)
            remove_perm('change_team', instance.captain, instance)
            remove_perm('delete_team', instance.captain, instance)

        return super(TeamFullSerializer, self).update(instance, validated_data)


class TeamContestsHistorySerializer(serializers.ModelSerializer, ReadOnlySerializerMixin):
    contest_title = serializers.SlugRelatedField(
        read_only=True,
        slug_field='title',
        source='contest',
    )
    registered_users_details = api.users.serializers.UserMinimalSerializer(
        many=True,
        read_only=True,
        source='registered_users',
    )

    class Meta:
        model = api.models.ContestParticipantRelationship
        fields = (
            'id',
            'contest',
            'contest_title',
            'delta',
            'opened_contest_at',
            'registered_users_details',
        )


class TeamJoinSerializer(serializers.ModelSerializer, ReadOnlySerializerMixin):
    class Meta:
        model = api.models.Team
        fields = ('join_token',)

    def validate_join_token(self, join_token):
        if join_token != self.instance.join_token:
            raise serializers.ValidationError('Invalid join token.')
