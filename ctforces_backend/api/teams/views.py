from django.db.models import Avg
from rest_framework import viewsets as rest_viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from api import mixins as api_mixins
from api import models as api_models
from api import pagination as api_pagination
from api.teams import permissions as api_teams_permissions
from api.teams import serializers as api_teams_serializers


class TeamViewSet(api_mixins.CustomPermissionsQuerysetViewSetMixin,
                  api_mixins.CustomPermissionsViewSetMixin,
                  rest_viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = api_pagination.TeamDefaultPagination
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    queryset = api_models.Team.objects.all()

    action_permission_classes = {
        'update': (api_teams_permissions.HasEditTeamPermission,),
        'partial_update': (api_teams_permissions.HasEditTeamPermission,),
        'destroy': (api_teams_permissions.HasDeleteTeamPermission,),
        'get_full': (api_teams_permissions.HasEditTeamPermission,),
    }

    klass = api_models.Team

    action_permissions_querysets = {
        'update': 'change_team',
        'partial_update': 'change_team',
        'destroy': 'delete_team',
    }

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
        queryset = api_models.ContestParticipantRelationship.objects.filter(
            participant=instance,
        )
        serializer = api_teams_serializers.TeamContestsHistorySerializer(queryset)
        return Response(serializer.data)
