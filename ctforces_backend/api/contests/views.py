from collections import defaultdict

from django.db.models import Count, Value as V, OuterRef, Exists, F, Prefetch, IntegerField, Avg
from django.db.models.functions import Coalesce
from django.utils import timezone
from ratelimit.decorators import ratelimit
from rest_framework import mixins as rest_mixins
from rest_framework import viewsets as rest_viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError, Throttled
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework_extensions.cache.decorators import cache_response

import api.contests.permissions
import api.contests.serializers
import api.models
import api.pagination
import api.tasks.serializers
import api.teams.serializers
from api.contests.caching import CTFTimeScoreboardKeyConstructor
from api.database_functions import SubquerySum
from api.mixins import (
    CustomPermissionsQuerysetViewSetMixin,
    CustomPermissionsViewSetMixin,
)


class ContestViewSet(CustomPermissionsViewSetMixin,
                     CustomPermissionsQuerysetViewSetMixin,
                     rest_viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = api.pagination.ContestDefaultPagination
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    queryset = api.models.Contest.objects.order_by('-start_time')

    action_permission_classes = {
        'retrieve': (api.contests.permissions.HasViewContestPermission,),
        'get_full_contest': (api.contests.permissions.HasEditContestPermission,),
        'create': (api.contests.permissions.HasCreateContestPermission,),
        'update': (api.contests.permissions.HasEditContestPermission,),
        'partial_update': (api.contests.permissions.HasEditContestPermission,),
        'destroy': (api.contests.permissions.HasDeleteContestPermission,),
    }

    klass = api.models.Contest
    action_permissions_querysets = {
        'update': 'change_contest',
        'partial_update': 'change_contest',
        'destroy': 'delete_contest',
    }

    def get_participating_team(self, contest):
        if hasattr(self.request, 'team_participant'):
            return self.request.team_participant

        relation = contest.contest_participant_relationship.filter(
            registered_users_id=self.request.user.id,
        ).first()

        self.request.team_participant = getattr(relation, 'participant', None)
        return self.request.team_participant

    def get_queryset(self):
        queryset = super(ContestViewSet, self).get_queryset()

        if self.action == 'list':
            queryset = queryset.filter(
                is_published=True,
            ).annotate(
                is_registered=Exists(
                    api.models.ContestParticipantRelationship.objects.filter(
                        registered_users__id=self.request.user.id,
                        contest=OuterRef('id'),
                    )
                ),
            )

        return queryset.annotate(
            registered_count=Count('participants', distinct=True),
        )

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return api.contests.serializers.ContestViewSerializer
        if self.action == 'list':
            return api.contests.serializers.ContestPreviewSerializer
        return api.contests.serializers.ContestFullSerializer

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

        paginator, finished = api.pagination.get_paginated_data(
            api.pagination.ContestDefaultPagination(),
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
        serializer = api.contests.serializers.ContestFullSerializer(instance=instance)
        return Response(serializer.data)

    @staticmethod
    def get_scoreboard_for_participants_page(paginator, participants_page, contest: api.models.Contest):
        page_ids = list(map(lambda x: x.id, participants_page))

        relationship_queryset = api.models.ContestTaskRelationship.objects.filter(
            contest=contest,
        ).prefetch_related(
            Prefetch(
                'solved_by',
                queryset=api.models.Team.objects.filter(id__in=page_ids).only('id'),
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

        teams_serializer = api.contests.serializers.ContestScoreboardParticipantSerializer(
            instance=participants_page,
            many=True,
        )

        teams_data = paginator.get_paginated_response(teams_serializer.data).data

        return Response({
            'participants': teams_data,
            'main_data': result_data,
        })

    @staticmethod
    def get_scoreboard_relations_queryset(contest):
        if contest.dynamic_scoring:
            manager = api.models.ContestTaskRelationship.dynamic_current_cost_annotated
        else:
            manager = api.models.ContestTaskRelationship.static_current_cost_annotated

        participant_cost_sum_subquery = SubquerySum(
            manager.filter(
                contest=contest,
                solved_by__id=OuterRef('participant_id'),
            ).values('current_cost'),
            output_field=IntegerField(),
            field_name='current_cost',
        )

        relations = api.models.ContestParticipantRelationship.objects.filter(
            contest=contest,
        ).select_related(
            'participant',
        ).prefetch_related('registered_users').annotate(
            cost_sum=Coalesce(participant_cost_sum_subquery, V(0)),
            rating=Avg('registered_users__rating', distinct=True),
        ).only(
            'participant',
            'last_solve',
            'registered_users',
        ).order_by('-cost_sum', 'last_solve')

        return relations

    def get_ordered_scoreboard_users_page(self, contest):
        relations_queryset = self.get_scoreboard_relations_queryset(contest)

        users_paginator = api.pagination.ScoreboardPagination()
        relations_page = users_paginator.paginate_queryset(
            queryset=relations_queryset,
            request=self.request,
        )

        participants = []
        for relation in relations_page:
            participant = relation.participant
            participant.rating = relation.rating
            participant.registered_users = relation.registered_users
            participant.cost_sum = relation.cost_sum
            participant.last_contest_solve = relation.last_solve
            participants.append(participant)

        return self.get_scoreboard_for_participants_page(
            paginator=users_paginator,
            participants_page=participants,
            contest=contest,
        )

    @action(detail=True,
            url_name='registrations',
            url_path='registrations',
            methods=['get'])
    def get_registrations(self, *_args, **_kwargs):
        contest = self.get_object()
        queryset = api.models.ContestParticipantRelationship.objects.filter(
            contest=contest,
        ).prefetch_related(
            'registered_users'
        ).annotate(
            rating=Avg('registered_users__rating', distinct=True),
        ).order_by('-id')
        paginator = api.pagination.ContestRegistrationsPagination()
        page = paginator.paginate_queryset(queryset=queryset, request=self.request)
        serializer = api.contests.serializers.CPRSerializer(page, many=True)
        return Response(serializer.data)

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
        timeout=60,
        key_func=CTFTimeScoreboardKeyConstructor(),
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
                'team': relation.participant.name,
                'score': relation.cost_sum,
                'lastAccept': int(relation.last_solve.timestamp()),
            })

        return Response({'standings': standings})


class ContestParticipantRelationshipViewSet(rest_viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = api.models.ContestParticipantRelationship.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    serializer_class = api.contests.serializers.CPRSerializer

    def get_queryset(self):
        qs = super(ContestParticipantRelationshipViewSet, self).get_queryset()
        return qs.filter(participant_id__in=self.request.user.teams.only('id'))


class ContestTaskRelationshipViewSet(CustomPermissionsViewSetMixin,
                                     rest_mixins.RetrieveModelMixin,
                                     rest_mixins.CreateModelMixin,
                                     rest_mixins.UpdateModelMixin,
                                     rest_mixins.DestroyModelMixin,
                                     rest_viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = api.models.ContestTaskRelationship.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    serializer_class = api.contests.serializers.CTRMainSerializer

    action_permission_classes = {
        'create': (api.contests.permissions.HasContestTaskRelationshipPermission,),
        'update': (api.contests.permissions.HasContestTaskRelationshipPermission,),
        'partial_update': (api.contests.permissions.HasContestTaskRelationshipPermission,),
        'destroy': (api.contests.permissions.HasContestTaskRelationshipPermission,),
    }

    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'partial_update':
            return api.contests.serializers.CTRUpdateSerializer
        return super(ContestTaskRelationshipViewSet, self).get_serializer_class()

    def get_serializer(self, *args, **kwargs):
        if self.action == 'create':
            kwargs['many'] = isinstance(self.request.data, list)
        return super(ContestTaskRelationshipViewSet, self).get_serializer(*args, **kwargs)


class ContestTaskViewSet(rest_viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = api.contests.serializers.ContestTaskPreviewSerializer
    lookup_field = 'task_id'
    lookup_url_kwarg = 'task_id'
    queryset = api.models.Task.objects.all()

    def get_participating_team(self, contest):
        if hasattr(self.request, 'team_participant'):
            return self.request.team_participant

        self.request.team_participant = contest.participants.filter(
            id__in=self.request.user.teams.only('id'),
        ).first()
        return self.request.team_participant

    def get_contest(self):
        contest_id = self.kwargs.get('contest_id')

        try:
            contest_id = int(contest_id)
        except ValueError:
            raise ValidationError(detail='Invalid contest_id.')

        contest = api.models.Contest.objects.filter(
            id=contest_id
        ).prefetch_related(
            'tasks',
            'participants',
        ).first()

        if not contest:
            raise NotFound(detail='Contest not found.')

        can_view = self.request.user.has_perm('view_contest', contest)

        if not can_view:
            if not contest.is_published:
                raise NotFound(detail='Contest not found.')

            if not contest.is_running and not contest.is_finished:
                raise PermissionDenied(detail='Contest is not started yet')

        team = self.get_participating_team(contest)
        if not can_view and not contest.is_finished and team is None:
            raise PermissionDenied(detail='Register for a contest first')

        if self.action == 'retrieve':
            api.models.ContestParticipantRelationship.objects.filter(
                contest=contest,
                participant=team,
            ).update(has_opened_contest=True)

        return contest

    def get_queryset(self):
        contest = self.get_contest()

        if contest.dynamic_scoring:
            manager = api.models.ContestTaskRelationship.dynamic_current_cost_annotated
        else:
            manager = api.models.ContestTaskRelationship.static_current_cost_annotated

        contest_task_relationship_query = manager.prefetch_related(
            'task__tags',
        ).select_related(
            'task__author',
            'main_tag',
        ).order_by(
            'ordering_number',
            'cost',
            'task_id',
        )

        if self.action in ['retrieve', 'get_solved', 'submit_flag']:
            return contest_task_relationship_query

        all_solved = set(
            api.models.ContestTaskRelationship.objects.filter(
                contest=contest,
                solved_by=self.get_participating_team(contest),
            ).values_list('task_id', flat=True)
        )

        tasks = []
        for relation in contest_task_relationship_query:
            task = relation.task

            if task.id in all_solved:
                task.is_solved_by_user = True
            else:
                task.is_solved_by_user = False

            task.main_tag = relation.main_tag
            task.contest_cost = relation.current_cost
            task.ordering_number = relation.ordering_number

            tasks.append(task)

        if self.action == 'list':
            counts = api.models.ContestTaskRelationship.objects.filter(
                contest=contest,
            ).annotate(
                solved_count=Coalesce(
                    Count(
                        'solved_by',
                        distinct=True,
                    ),
                    V(0),
                ),
            ).values_list('id', 'solved_count')

            per_task_solves = {count[0]: count[1] for count in counts}

            for task in tasks:
                task.solved_count = per_task_solves.get(task.id, 0)

        return tasks

    def get_object(self):
        task_id = self.kwargs.get('task_id')

        try:
            task_id = int(task_id)
            if task_id < 1:
                raise ValueError()
        except ValueError:
            raise ValidationError(detail='Invalid task_id.')

        try:
            task = self.get_queryset().get(task_id=task_id).task
        except api.models.ContestTaskRelationship.DoesNotExist:
            raise NotFound('No such task.')

        if self.action == 'retrieve' and self.request.user.has_perm('change_task', task):
            task.can_edit_task = True

        return task

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return api.contests.serializers.ContestTaskViewSerializer
        return super(ContestTaskViewSet, self).get_serializer_class()

    @action(detail=True,
            url_name='solved',
            url_path='solved',
            methods=['get'])
    def get_solved(self, *_args, **_kwargs):
        task = self.get_object()
        contest = self.get_contest()
        solved_participants_queryset = api.models.ContestTaskRelationship.objects.get(
            task=task,
            contest=contest,
        ).solved_by.annotate(
            rating=Avg('participants__rating', distinct=True),
        ).order_by('-id').all()

        return api.pagination.get_paginated_response(
            paginator=api.pagination.UserDefaultPagination(),
            queryset=solved_participants_queryset,
            serializer_class=api.teams.serializers.TeamMinimalSerializer,
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
            raise ValidationError({'flag': 'You cannot submit this task'})

        contest = self.get_contest()
        team = self.get_participating_team(contest)
        relation = api.models.ContestTaskRelationship.objects.get(
            contest=contest,
            task=task,
        )

        if relation.solved_by.filter(id=team.id).exists():
            raise PermissionDenied('Task already solved.')

        serializer = api.tasks.serializers.TaskSubmitSerializer(
            data=self.request.data,
            instance=task,
        )

        if serializer.is_valid(raise_exception=True):
            if contest.is_running:
                relation.solved_by.add(team)
                contest.contest_participant_relationship.filter(
                    participant_id=self.request.user.id,
                ).update(
                    last_solve=timezone.now(),
                )

            task.solved_by.add(self.request.user)
            self.request.user.last_solve = timezone.now()
            self.request.user.save()

            return Response('accepted!')
