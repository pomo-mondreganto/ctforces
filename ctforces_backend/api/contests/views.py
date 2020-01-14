from collections import defaultdict

from django.db.models import Count, Value as V, OuterRef, Exists, F, Q, Prefetch, IntegerField
from django.db.models.functions import Coalesce, Ceil, Greatest
from django.utils import timezone
from ratelimit.decorators import ratelimit
from rest_framework import mixins as rest_mixins
from rest_framework import serializers as rest_serializers
from rest_framework import viewsets as rest_viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError, Throttled
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework_extensions.cache.decorators import cache_response

from api import database_functions as api_database_functions
from api import mixins as api_mixins
from api import models as api_models
from api import pagination as api_pagination
from api.contests import (
    permissions as api_contests_permissions,
    serializers as api_contests_serializers,
    caching as api_contests_caching,
)
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
            is_solved_by_user_subquery = Exists(
                api_models.ContestTaskRelationship.objects.filter(
                    contest=OuterRef('contest_id'),
                    task=OuterRef('task_id'),
                    solved_by__id__exact=self.request.user.id
                )
            )

            prefetch = Prefetch(
                'contest_task_relationship',
                queryset=api_models.ContestTaskRelationship.objects.annotate(
                    solved_count=Coalesce(
                        Count('solved_by', distinct=True),
                        V(0),
                    ),
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

    @staticmethod
    def get_scoreboard_for_users_page(paginator, users_page, contest):
        user_ids = list(map(lambda x: x.id, users_page))

        relationship_queryset = api_models.ContestTaskRelationship.objects.filter(
            contest=contest,
        ).prefetch_related(
            Prefetch(
                'solved_by',
                queryset=api_models.User.objects.filter(id__in=user_ids).only('id'),
            )
        ).annotate(
            task_name=F('task__name'),
        )

        formatted_data = defaultdict(list)
        for relation in relationship_queryset:
            formatted_data[relation.task_name].extend(
                map(lambda x: x.id, relation.solved_by.all()),
            )

        result_data = list(
            dict(
                task_name=key,
                solved_participants=value
            ) for key, value in formatted_data.items()
        )

        users_serializer = api_contests_serializers.ContestScoreboardUserSerializer(
            instance=users_page,
            many=True,
        )

        users_data = paginator.get_paginated_response(users_serializer.data).data

        return Response({
            'users': users_data,
            'main_data': result_data,
        })

    @staticmethod
    def get_scoreboard_relations_queryset(contest):
        relation_filter = Q(contest=contest, participant__show_in_ratings=True)

        if contest.dynamic_scoring:
            user_cost_sum_subquery = api_database_functions.SubquerySum(
                api_models.ContestTaskRelationship.objects.filter(
                    contest=contest,
                ).annotate(
                    solved_count=Coalesce(
                        Count(
                            'solved_by',
                            distinct=True,
                        ),
                        V(0),
                    ),
                ).filter(
                    solved_by__id__exact=OuterRef('participant_id'),
                ).annotate(
                    current_cost=Greatest(
                        Ceil(
                            (F('min_cost') - F('max_cost')) /
                            (F('decay_value') * F('decay_value')) *
                            (F('solved_count') * F('solved_count')) +
                            F('max_cost')
                        ),
                        F('min_cost'),
                    ),
                ).values('current_cost'),
                output_field=IntegerField(),
                field_name='current_cost',
            )

        else:
            user_cost_sum_subquery = api_database_functions.SubquerySum(
                api_models.ContestTaskRelationship.objects.filter(
                    contest=contest,
                    solved_by__id__exact=OuterRef('id'),
                ).values('cost'),
                output_field=IntegerField(),
                field_name='cost',
            )

        relations = api_models.ContestParticipantRelationship.objects.filter(
            relation_filter,
        ).select_related(
            'participant',
        ).annotate(
            cost_sum=Coalesce(user_cost_sum_subquery, V(0)),
        ).only(
            'participant',
            'last_solve',
        ).order_by('-cost_sum', 'last_solve')

        return relations

    def get_ordered_scoreboard_users_page(self, contest):
        relations_queryset = self.get_scoreboard_relations_queryset(contest)

        users_paginator = api_pagination.UserScoreboardPagination()
        relations_page = users_paginator.paginate_queryset(
            queryset=relations_queryset,
            request=self.request,
        )

        participants = []
        for relation in relations_page:
            participant = relation.participant
            participant.cost_sum = relation.cost_sum
            participant.last_contest_solve = relation.last_solve
            participants.append(participant)

        return self.get_scoreboard_for_users_page(
            paginator=users_paginator,
            users_page=participants,
            contest=contest,
        )

    @action(
        detail=True,
        url_path='scoreboard',
        url_name='scoreboard',
        methods=['get'],
    )
    def get_scoreboard(self, _request, *_args, **_kwargs):
        contest = self.get_object()
        return self.get_ordered_scoreboard_users_page(contest)

    @cache_response(
        60,
        key_func=api_contests_caching.CTFTimeScoreboardKeyConstructor(),
    )
    @action(
        detail=True,
        url_path='ctftime_scoreboard',
        url_name='ctftime_scoreboard',
        methods=['get'],
    )
    def get_ctftime_scoreboard(self, _request, *_args, **_kwargs):
        contest = self.get_object()
        relations_queryset = self.get_scoreboard_relations_queryset(contest)

        standings = []
        for i, relation in enumerate(relations_queryset):
            standings.append({
                'pos': i + 1,
                'team': relation.participant.username,
                'score': relation.cost_sum,
                'lastAccept': int(relation.last_solve.timestamp()),
            })

        return Response({'standings': standings})

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
            api_models.ContestTaskRelationship.objects.filter(
                contest=contest,
                solved_by__id__exact=self.request.user.id,
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
            counts = api_models.ContestTaskRelationship.objects.filter(
                contest=contest,
            ).annotate(
                solved_count=Coalesce(
                    Count(
                        'solved_by',
                        distinct=True,
                    ),
                    V(0),
                ),
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
        solved_participants_queryset = api_models.ContestTaskRelationship.objects.get(
            task=task,
            contest=contest,
        ).solved_by.filter(show_in_ratings=True).all()

        return api_pagination.get_paginated_response(
            paginator=api_pagination.UserDefaultPagination(),
            queryset=solved_participants_queryset,
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

        relation = api_models.ContestTaskRelationship.objects.get(
            contest=contest,
            task=task,
        )

        if relation.solved_by.filter(id=self.request.user.id).exists():
            raise PermissionDenied('Task already solved.')

        serializer = api_tasks_serializers.TaskSubmitSerializer(
            data=self.request.data,
            instance=task,
        )

        if serializer.is_valid(raise_exception=True):
            if contest.is_running:
                relation.solved_by.add(self.request.user)

                contest.contest_participant_relationship.filter(
                    participant_id=self.request.user.id,
                ).update(
                    last_solve=timezone.now(),
                )

            task.solved_by.add(self.request.user)
            self.request.user.last_solve = timezone.now()
            self.request.user.save()

            return Response('accepted!')
