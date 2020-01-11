from collections import defaultdict

from django.db.models import Count, Value as V, Subquery, OuterRef, Exists, F, Prefetch, IntegerField
from django.db.models.functions import Coalesce
from django.utils import timezone
from ratelimit.decorators import ratelimit
from rest_framework import mixins as rest_mixins
from rest_framework import serializers as rest_serializers
from rest_framework import viewsets as rest_viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError, Throttled
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from api import database_functions as api_database_functions
from api import mixins as api_mixins
from api import models as api_models
from api import pagination as api_pagination
from api.contests import permissions as api_contests_permissions
from api.contests import serializers as api_contests_serializers
from api.tasks import serializers as api_tasks_serializers
from api.users import serializers as api_users_serializers


class ContestViewSet(api_mixins.CustomPermissionsViewSetMixin,
                     api_mixins.CustomPermissionsQuerysetViewSetMixin,
                     rest_viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = api_pagination.ContestDefaultPagination
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    queryset = api_models.Contest.objects.order_by('-start_time')

    action_permission_classes = {
        'retrieve': (api_contests_permissions.HasViewContestPermission,),
        'get_full_contest': (api_contests_permissions.HasEditContestPermission,),
        'create': (api_contests_permissions.HasCreateContestPermission,),
        'update': (api_contests_permissions.HasEditContestPermission,),
        'partial_update': (api_contests_permissions.HasEditContestPermission,),
        'destroy': (api_contests_permissions.HasDeleteContestPermission,),
        'register': (IsAuthenticated,)
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
            queryset = queryset.filter(
                is_published=True,
            ).annotate(
                is_registered=Exists(
                    api_models.ContestParticipantRelationship.objects.filter(
                        participant_id=self.request.user.id,
                        contest=OuterRef('id'),
                    )
                ),
            )

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
                    participant_id=self.request.user.id,
                ).only('id')
            )

            prefetch = Prefetch(
                'contest_task_relationship',
                queryset=api_models.ContestTaskRelationship.objects.annotate(
                    solved_count=solved_count_subquery,
                    is_solved_by_user=is_solved_by_user_subquery,
                ).select_related('task', 'main_tag').order_by('ordering_number'),
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
            obj.can_edit_contest = self.request.user.has_perm('change_contest', obj)
        return obj

    def list(self, request, *args, **kwargs):
        all_contests = self.get_queryset()
        upcoming_queryset = list(filter(lambda x: not x.is_running and not x.is_finished, all_contests))
        running_queryset = list(filter(lambda x: x.is_running, all_contests))
        finished_queryset = list(filter(lambda x: x.is_finished, all_contests))

        upcoming = self.get_serializer(upcoming_queryset, many=True).data
        running = self.get_serializer(running_queryset, many=True).data

        paginator, finished = api_pagination.get_paginated_data(
            api_pagination.ContestDefaultPagination(),
            finished_queryset,
            self.get_serializer_class(),
            request,
        )

        if paginator:
            finished = paginator.get_paginated_response(finished).data

        response_data = {
            'upcoming': upcoming,
            'running': running,
            'finished': finished,
        }

        return Response(response_data)

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

        # TODO: consider caching the whole scoreboard for N secs
        # TODO: consider using group by (similar to contest task) to fetch users top
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

        users_queryset = instance.participants.filter(
            show_in_ratings=True,
        )

        if self.request.query_params.get('group_id'):
            users_queryset = users_queryset.filter(
                groups__id=self.request.query_params['group_id']
            )

        users_queryset = users_queryset.annotate(
            cost_sum=Coalesce(
                user_cost_sum_subquery,
                V(0),
            ),
            last_contest_solve=last_contest_solve_subquery,
        ).order_by('-cost_sum', 'last_contest_solve').only(
            'username',
        )

        users_paginator = api_pagination.UserScoreboardPagination()

        users_page = users_paginator.paginate_queryset(
            queryset=users_queryset,
            request=self.request,
        )

        relationship_queryset = api_models.ContestTaskParticipantSolvedRelationship.objects.filter(
            contest=instance,
            participant__in=users_page,
        ).select_related('task').annotate(
            task_name=F('task__name'),
        )

        users_serializer = api_contests_serializers.ContestScoreboardUserSerializer(
            instance=users_page,
            many=True,
        )

        users_data = users_paginator.get_paginated_response(users_serializer.data).data

        data_serializer = api_contests_serializers.ContestScoreboardSerializer(
            instance=list(relationship_queryset),
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
            'users': users_data,
            'main_data': result_data,
        })

    @action(
        detail=True,
        url_path='register',
        url_name='register',
        methods=['get'],
    )
    def register(self, *_args, **_kwargs):
        contest = self.get_object()
        if not contest.is_published or not contest.is_registration_open:
            raise NotFound("Contest doesn't exist or registration isn't open yet")

        if self.request.user.has_perm('api.change_contest', contest):
            raise ValidationError(detail='You cannot register for this contest')

        api_models.ContestParticipantRelationship.objects.create(
            contest=contest,
            participant=self.request.user,
        )

        return Response('ok')


class ContestTaskRelationshipViewSet(api_mixins.CustomPermissionsViewSetMixin,
                                     rest_mixins.RetrieveModelMixin,
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
        'create': (api_contests_permissions.HasContestTaskRelationshipPermission,),
        'update': (api_contests_permissions.HasContestTaskRelationshipPermission,),
        'partial_update': (api_contests_permissions.HasContestTaskRelationshipPermission,),
        'destroy': (api_contests_permissions.HasContestTaskRelationshipPermission,),
    }

    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'partial_update':
            return api_contests_serializers.ContestTaskRelationshipUpdateSerializer
        return super(ContestTaskRelationshipViewSet, self).get_serializer_class()

    def get_serializer(self, *args, **kwargs):
        if self.action == 'create':
            kwargs['many'] = isinstance(self.request.data, list)
        return super(ContestTaskRelationshipViewSet, self).get_serializer(*args, **kwargs)


# TODO: contest task listing & individual tasks can be cached (logged in as a key bit)
class ContestTaskViewSet(rest_viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = api_contests_serializers.ContestTaskPreviewSerializer
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
            raise NotFound(detail='Contest not found.')

        if not contest.is_running and not contest.is_finished:
            if not self.request.user.has_perm('view_contest', contest):
                raise PermissionDenied(detail='Contest is not started yet')

        if self.action == 'retrieve':
            api_models.ContestParticipantRelationship.objects.filter(
                contest=contest,
                participant_id=self.request.user.id,
            ).update(has_opened_contest=True)

        return contest

    def get_queryset(self):
        contest = self.get_contest()

        contest_task_relationship_query = api_models.ContestTaskRelationship.objects.filter(
            contest=contest
        ).prefetch_related('task__tags').select_related('task__author').order_by(
            'ordering_number',
            'cost',
            'task_id',
        )

        all_solved_by_user = set(
            api_models.ContestTaskParticipantSolvedRelationship.objects.filter(
                contest=contest,
                participant_id=self.request.user.id,
            ).values_list('task_id', flat=True)
        )

        tasks = []
        for relation in contest_task_relationship_query:
            task = relation.task

            if task.id in all_solved_by_user:
                task.is_solved_by_user = True

            task.contest_cost = relation.cost
            task.ordering_number = relation.ordering_number

            tasks.append(task)

        if self.action == 'list':
            counts = api_models.ContestTaskParticipantSolvedRelationship.objects.filter(
                contest=contest,
            ).values_list(
                'contest_id',
                'task_id',
            ).annotate(
                solved_count=Coalesce(Count('participant_id', distinct=True), V(0)),
            )

            per_task_solves = {count[1]: count[2] for count in counts}

            for task in tasks:
                task.solved_count = per_task_solves.get(task.id, 0)

        return tasks

    def get_object(self):
        task_number = self.kwargs.get('task_number')

        try:
            task_number = int(task_number)
            if task_number < 1:
                raise ValueError()
        except ValueError:
            raise ValidationError(detail='Invalid task_number.')

        try:
            task = self.get_queryset()[task_number - 1]
        except IndexError:
            raise NotFound('No such task.')

        if self.action == 'retrieve' and self.request.user.has_perm('change_task', task):
            task.real_id = task.id
            task.can_edit_task = True

        return task

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return api_contests_serializers.ContestTaskViewSerializer
        return super(ContestTaskViewSet, self).get_serializer_class()

    @action(detail=True,
            url_name='solved',
            url_path='solved',
            methods=['get'])
    def get_solved(self, *_args, **_kwargs):
        task = self.get_object()
        contest = self.get_contest()
        solved_participants_queryset = api_models.ContestTaskParticipantSolvedRelationship.objects.filter(
            task=task,
            contest=contest,
            participant__show_in_ratings=True,
        ).select_related('participant')

        users_solved = list(map(lambda x: x.participant, solved_participants_queryset))

        return api_pagination.get_paginated_response(
            paginator=api_pagination.UserDefaultPagination(),
            queryset=users_solved,
            serializer_class=api_users_serializers.UserBasicSerializer,
            request=self.request,
        )

    @action(detail=True,
            url_name='submit',
            url_path='submit',
            methods=['post'])
    @ratelimit(key='user', rate='4/m')
    def submit_flag(self, *_args, **_kwargs):
        if getattr(self.request, 'limited', False):
            raise Throttled(detail='You can submit flag 4 times per minute.')

        task = self.get_object()

        if self.request.user.has_perm('api.change_task', task):
            raise rest_serializers.ValidationError(
                {
                    'flag': 'You cannot submit that task',
                },
            )

        contest = self.get_contest()
        if contest.is_running and not contest.participants.filter(
            id=self.request.user.id,
        ).exists():
            raise PermissionDenied('You are not registered for this contest.')

        if api_models.ContestTaskParticipantSolvedRelationship.objects.filter(
            contest=contest,
            task=task,
            participant_id=self.request.user.id,
        ).exists():
            raise PermissionDenied('Task already solved.')

        serializer = api_tasks_serializers.TaskSubmitSerializer(
            data=self.request.data,
            instance=task,
        )

        if serializer.is_valid(raise_exception=True):
            if contest.is_running:
                api_models.ContestTaskParticipantSolvedRelationship.objects.create(
                    contest=contest,
                    task=task,
                    participant_id=self.request.user.id,
                )

                contest.contest_participant_relationship.filter(
                    participant_id=self.request.user.id,
                ).update(
                    last_solve=timezone.now(),
                )

            task.solved_by.add(self.request.user)
            self.request.user.last_solve = timezone.now()
            self.request.user.save()

            return Response('accepted!')
