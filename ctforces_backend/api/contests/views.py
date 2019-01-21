from collections import defaultdict

from django.db.models import Count, Value as V, Subquery, OuterRef, Exists, F, Q, Prefetch, IntegerField
from django.db.models.functions import Coalesce
from django.utils import timezone
from ratelimit.decorators import ratelimit
from rest_framework import mixins as rest_mixins
from rest_framework import viewsets as rest_viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError, Throttled
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from api import database_functions as api_database_functions
from api import mixins as api_mixins
from api import models as api_models
from api import pagination as api_pagination
from api import permissions as api_permissions
from api.contests import serializers as api_contests_serializers
from api.tasks import serializers as api_tasks_serializers


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

        if self.action == 'retrieve' or self.action == 'get_full_contest':
            solved_count_subquery = api_database_functions.SubqueryCount(
                api_models.ContestTaskParticipantSolvedRelationship.objects.filter(
                    contest=OuterRef('contest_id'),
                    task=OuterRef('task_id'),
                ).only('id')
            )

            is_solved_by_user_subquery = Exists(
                api_models.ContestTaskParticipantSolvedRelationship.objects.filter(
                    contest=OuterRef('contest_id'),
                    task=OuterRef('task_id'),
                    participant=self.request.user,
                ).only('id')
            )

            prefetch = Prefetch(
                'contest_task_relationship',
                queryset=api_models.ContestTaskRelationship.objects.annotate(
                    solved_count=solved_count_subquery,
                    is_solved_by_user=is_solved_by_user_subquery,
                ).select_related('task'),
            )
            queryset = queryset.prefetch_related(prefetch)

        return queryset.annotate(
            registered_count=Count('participants', distinct=True),
        )

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return api_contests_serializers.ContestViewSerializer
        if self.action == 'list':
            return api_contests_serializers.ContestPreviewSerializer
        return api_contests_serializers.ContestFullSerializer

    def get_object(self):
        obj = super(ContestViewSet, self).get_object()
        if self.action == 'retrieve':
            obj.can_edit_task = self.request.user.has_perm('change_contest', obj)
        return obj

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

        contest_cost_subquery = Subquery(
            api_models.ContestTaskRelationship.objects.filter(
                contest_id=instance.id,
                task_id=OuterRef('task_id'),
            ).values('cost'),
            output_field=IntegerField(),
        )

        user_cost_sum_subquery = api_database_functions.SubquerySum(
            api_models.ContestTaskParticipantSolvedRelationship.objects.filter(
                contest_id=instance.id,
                participant_id=OuterRef('id'),
            ).annotate(
                cost=Coalesce(
                    contest_cost_subquery,
                    V(0),
                )
            ).values('cost'),
            output_field=IntegerField(),
            field_name='cost',
        )

        last_contest_solve_subquery = Subquery(
            api_models.ContestParticipantRelationship.objects.filter(
                contest=instance,
                participant=OuterRef('id'),
            ).values('last_solve')
        )

        users_queryset = instance.participants.annotate(
            cost_sum=Coalesce(
                user_cost_sum_subquery,
                V(0),
            ),
            last_contest_solve=last_contest_solve_subquery,
        ).order_by('-cost_sum', 'last_contest_solve').only(
            'username',
        )

        users_paginator = api_pagination.UserScoreboardPagination()

        users_page = users_paginator.paginate_queryset(queryset=users_queryset, request=self.request)
        if users_page is None:
            users_page = list(users_queryset)

        relationship_queryset = api_models.ContestTaskParticipantSolvedRelationship.objects.filter(
            contest=instance,
            participant__in=users_page,
        ).select_related('task').annotate(
            task_name=F('task__name'),
        )

        data_serializer = api_contests_serializers.ContestScoreboardSerializer(
            instance=list(relationship_queryset),
            many=True,
        )

        users_serializer = api_contests_serializers.ContestScoreboardUserSerializer(
            instance=users_page,
            many=True,
        )

        solved_tasks_data = data_serializer.data

        reformatted_data = defaultdict(list)

        for element in solved_tasks_data:
            reformatted_data[element['task_name']].append(element['participant_id'])

        result_data = list(
            dict(
                task_name=key,
                solved_participants=value
            ) for key, value in reformatted_data.items()
        )

        return Response({
            'users': users_serializer.data,
            'main_data': result_data,
        })


class ContestTaskRelationshipViewSet(api_mixins.CustomPermissionsViewSetMixin,
                                     rest_mixins.CreateModelMixin,
                                     rest_mixins.UpdateModelMixin,
                                     rest_mixins.DestroyModelMixin,
                                     rest_viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = api_models.ContestTaskRelationship.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    serializer_class = api_contests_serializers.ContestTaskRelationshipMainSerializer

    action_permission_classes = {
        'create': (api_permissions.HasCreateContestPermission,),
        'update': (api_permissions.HasContestTaskRelationshipPermission,),
        'partial_update': (api_permissions.HasContestTaskRelationshipPermission,),
        'destroy': (api_permissions.HasContestTaskRelationshipPermission,),
    }

    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'partial_update':
            return api_contests_serializers.ContestTaskRelationshipUpdateSerializer
        return super(ContestTaskRelationshipViewSet, self).get_serializer_class()

    def get_serializer(self, *args, **kwargs):
        if self.action == 'create':
            kwargs['many'] = isinstance(self.request.data, list)
        return super(ContestTaskRelationshipViewSet, self).get_serializer(*args, **kwargs)


class ContestTaskViewSet(rest_viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = api_contests_serializers.ContestTaskViewSerializer
    lookup_field = 'task_number'
    lookup_url_kwarg = 'task_number'

    queryset = api_models.Task.objects.all()

    def get_contest(self):
        contest_id = self.kwargs.get('contest_id')

        try:
            contest_id = int(contest_id)
        except ValueError:
            raise ValidationError(detail='Invalid contest_id.')

        contest = api_models.Contest.objects.filter(
            id=contest_id
        ).prefetch_related(
            'tasks',
        ).first()
        if not contest:
            raise NotFound(detail='Contest not found.')

        if not contest.is_published and not self.request.user.has_perm('view_contest', contest):
            raise PermissionDenied(detail='You cannot access this contest')

        return contest

    def get_queryset(self):
        contest = self.get_contest()

        contest_task_relationship_subquery = api_models.ContestTaskRelationship.objects.filter(
            contest=contest
        )

        queryset = api_models.Task.objects.filter(
            contest_task_relationship__in=contest_task_relationship_subquery
        ).annotate(
            is_solved_by_user=Exists(
                api_models.ContestTaskParticipantSolvedRelationship.objects.filter(
                    task_id=OuterRef('id'),
                    contest=contest,
                    participant=self.request.user.id,
                ),
            ),
            solved_count=Count(
                'contest_task_participant_solved_relationship',
                filter=Q(contest_id=contest.id),
                distinct=True,
            ),
            contest_cost=Subquery(
                api_models.ContestTaskRelationship.objects.filter(
                    contest=contest,
                    task_id=OuterRef('id')
                ).values('cost')
            )
        ).prefetch_related('tags', 'files')

        return queryset

    def get_object(self):
        task_number = self.kwargs.get('task_number')

        try:
            task_number = int(task_number)
            if task_number < 1:
                raise ValueError()
        except ValueError:
            raise ValidationError(detail='Invalid task_number.')
        queryset = self.get_queryset()[task_number - 1:task_number]
        task = queryset.first()

        if not task:
            raise NotFound('No such task.')

        return task

    @action(detail=True,
            url_name='submit',
            url_path='submit',
            methods=['post'])
    @ratelimit(key='user', rate='4/m')
    def submit_flag(self, *_args, **_kwargs):
        if getattr(self.request, 'limited', False):
            raise Throttled(detail='You can submit flag 4 times per minute.')

        task = self.get_object()
        contest = self.get_contest()
        if contest.is_running and not contest.participants.filter(id=self.request.user.id).exists():
            raise PermissionDenied('You are not registered.')

        if api_models.ContestTaskParticipantSolvedRelationship.objects.filter(
            contest=contest,
            task=task,
            participant=self.request.user.id,
        ).exists():
            raise PermissionDenied('Task already solved.')

        serializer = api_tasks_serializers.TaskSubmitSerializer(data=self.request.data, instance=task)
        if serializer.is_valid(raise_exception=True):
            if contest.is_running:
                api_models.ContestTaskParticipantSolvedRelationship.objects.create(
                    contest=contest,
                    task=task,
                    participant=self.request.user.id,
                )

                contest.contest_participant_relationship.filter(
                    participant=self.request.user.id,
                ).update(
                    last_solve=timezone.now(),
                )

            task.solved_by.add(self.request.user)
            api_models.User.objects.filter(id=self.request.user.id).update(
                last_solve=timezone.now()
            )

            return Response('accepted!')
