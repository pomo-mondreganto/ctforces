from django.db.models import Avg
from guardian.shortcuts import assign_perm
from rest_framework import viewsets as rest_viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

import api.models
from api import pagination as api_pagination
from api.mixins import CustomPermissionsViewSetMixin
from api.teams import permissions as api_teams_permissions
from api.teams import serializers as api_teams_serializers


class TeamViewSet(CustomPermissionsViewSetMixin,
                  rest_viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = api_pagination.TeamDefaultPagination
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    queryset = api.models.Team.objects.all()

    action_permission_classes = {
        'update': (api_teams_permissions.HasEditTeamPermission,),
        'partial_update': (api_teams_permissions.HasEditTeamPermission,),
        'destroy': (api_teams_permissions.HasDeleteTeamPermission,),
        'get_full': (api_teams_permissions.HasEditTeamPermission,),
        'kick': (api_teams_permissions.HasEditTeamPermission,),
    }

    klass = api.models.Team

    def get_queryset(self):
        qs = super(TeamViewSet, self).get_queryset()
        qs = qs.select_related(
            'captain',
        ).prefetch_related(
            'participants',
        ).annotate(
            rating=Avg('participants__rating', distinct=True),
        )
        return qs

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return api_teams_serializers.TeamViewSerializer
        if self.action == 'list':
            return api_teams_serializers.TeamMinimalSerializer
        return api_teams_serializers.TeamFullSerializer

    def get_object(self):
        obj = super(TeamViewSet, self).get_object()
        if self.action == 'retrieve':
            obj.can_edit_team = self.request.user.has_perm('change_team', obj)
            obj.can_delete_team = self.request.user.has_perm('delete_team', obj)
        return obj

    @action(
        detail=True,
        url_path='full',
        url_name='full',
        methods=['get'],
    )
    def get_full(self, request, *args, **kwargs):
        return super(TeamViewSet, self).retrieve(request, *args, **kwargs)

    @action(
        detail=True,
        url_path='contests',
        url_name='contests',
        methods=['get'],
    )
    def get_contests_history(self, request, *args, **kwargs):
        instance = self.get_object()
        queryset = api.models.ContestParticipantRelationship.objects.filter(
            participant=instance,
        ).select_related(
            'contest',
        ).prefetch_related(
            'registered_users',
        )

        serializer = api_teams_serializers.TeamContestsHistorySerializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        url_path='kick',
        url_name='kick',
        methods=['post'],
    )
    def kick_member(self, _request, *_args, **_kwargs):
        team = self.get_object()
        participant_id = self.request.data.get('participant_id')
        try:
            team_member = team.participants.get(id=participant_id)
        except (api.models.User.DoesNotExist, ValueError, TypeError):
            raise NotFound("No such team member")

        if team_member == team.captain:
            raise ValidationError({'participant_id': 'You cannot kick the captain'})

        team.participants.remove(team_member)
        team.join_token = team.gen_join_token(team.name)
        team.save()

        return Response('ok')

    @action(
        detail=True,
        url_path='join',
        url_name='join',
        methods=['post'],
    )
    def join_team(self, _request, *_args, **_kwargs):
        team = self.get_object()
        token = self.request.data.get('join_token')

        if token != team.join_token:
            raise ValidationError({'join_token': 'Invalid token'})

        team.participants.add(self.request.user)
        assign_perm('register_team', self.request.user, team)

        return Response('ok')
