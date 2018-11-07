from django.db.models import Count, Sum, Case, When, IntegerField, Value as V, Subquery, OuterRef
from rest_framework import mixins as rest_mixins
from rest_framework import status
from rest_framework import viewsets as rest_viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from api import mixins as api_mixins
from api import models as api_models
from api import pagination as api_pagination
from api import permissions as api_permissions
from api.contests import serializers as api_contests_serializers


class ContestViewSet(api_mixins.CustomPermissionsViewSetMixin,
                     api_mixins.CustomPermissionsQuerysetViewSetMixin,

                     rest_viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = api_pagination.ContestDefaultPagination
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    queryset = api_models.Contest.objects.order_by('-start_time')

    action_permission_classes = {
        'retrieve': (api_permissions.HasViewContestPermission,),
        'get_full_contest': (api_permissions.HasEditContestPermission,),
        'create': (api_permissions.HasCreateContestPermission,),
        'update': (api_permissions.HasEditContestPermission,),
        'partial_update': (api_permissions.HasEditContestPermission,),
        'destroy': (api_permissions.HasDeleteContestPermission,),
    }

    klass = api_models.Contest
    action_permissions_querysets = {
        'update': 'change_contest',
        'partial_update': 'change_contest',
        'destroy': 'delete_contest',
    }

    def get_queryset(self):
        queryset = super(ContestViewSet, self).get_queryset()

        if self.action == 'list':
            queryset = queryset.filter(is_published=True)

        return queryset.annotate(
            registered_count=Count('participants', distinct=True),
        )

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return api_contests_serializers.ContestViewSerializer
        if self.action == 'list':
            return api_contests_serializers.ContestPreviewSerializer
        return api_contests_serializers.ContestFullSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.can_edit_task = request.user.has_perm('change_contest')
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(
        detail=True,
        url_path='full',
        url_name='full',
        methods=['get'],
    )
    def get_full_contest(self, _request, *_args, **_kwargs):
        instance = self.get_object()
        serializer = api_contests_serializers.ContestFullSerializer(instance=instance)
        return Response(serializer.data)

    @action(
        detail=True,
        url_path='scoreboard',
        url_name='scoreboard',
        methods=['get'],
    )
    def get_scoreboard(self, _request, *_args, **_kwargs):
        instance = self.get_object()
        queryset = instance.participants.annotate(
            cost_sum=Sum(
                Case(
                    When(
                        contest_task_relationship__contest=instance,
                        then='contest_task_relationship__cost'
                    ),
                    default=V(0),
                    output_field=IntegerField()
                )
            ),
            solved_tasks=Subquery(
                api_models.ContestTaskRelationship.objects.filter(
                    contest=instance,
                    solved__id=OuterRef('id'),
                ).values('task__id')
            ),
        )

        paginator = api_pagination.UserScoreboardPagination()
        page = paginator.paginate_queryset(
            queryset=queryset,
            request=self.request,
        )

        serializer_class = api_contests_serializers.ContestScoreboardSerializer

        if page is not None:
            serializer = serializer_class(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data)


class ContestTaskRelationshipViewSet(api_mixins.CustomPermissionsViewSetMixin,
                                     rest_mixins.CreateModelMixin,
                                     rest_mixins.UpdateModelMixin,
                                     rest_mixins.DestroyModelMixin,
                                     rest_viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = api_models.ContestTaskRelationship.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    serializer_class = api_contests_serializers.ContestTaskRelationshipSerializer

    action_permission_classes = {
        'create': (api_permissions.HasCreateContestPermission,),
        'update': (api_permissions.HasContestTaskRelationshipPermission,),
        'partial_update': (api_permissions.HasContestTaskRelationshipPermission,),
        'destroy': (api_permissions.HasContestTaskRelationshipPermission,),
    }

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
