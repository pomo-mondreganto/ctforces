from collections import defaultdict

from django.db.models import F, Prefetch
from django.db.transaction import atomic
from django.utils import timezone
from ratelimit.decorators import ratelimit
from rest_framework import mixins as rest_mixins
from rest_framework import viewsets as rest_viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError, Throttled
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework_extensions.cache.decorators import cache_response

import api.contests.caching
import api.contests.permissions
import api.contests.serializers
import api.models
import api.pagination
import api.tasks.serializers
import api.teams.serializers
from api.mixins import CustomPermissionsViewSetMixin


class ContestViewSet(CustomPermissionsViewSetMixin,
                     rest_viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = api.pagination.ContestDefaultPagination
    lookup_field = 'id'
    queryset = api.models.Contest.objects.with_participant_count().order_by(
        '-start_time',
    ).select_related(
        'author',
    ).prefetch_related(
        'contest_task_relationship__task__tags',
    )

    action_permission_classes = {
        'retrieve': (api.contests.permissions.HasViewContestPermission,),
        'get_full_contest': (api.contests.permissions.HasEditContestPermission,),
        'create': (api.contests.permissions.HasCreateContestPermission,),
        'update': (api.contests.permissions.HasEditContestPermission,),
        'partial_update': (api.contests.permissions.HasEditContestPermission,),
        'destroy': (api.contests.permissions.HasDeleteContestPermission,),

        'get_scoreboard': (
            api.contests.permissions.HasViewContestPermission,
            api.contests.permissions.HasViewScoreboardPermission,
        ),
        'get_registrations': (
            api.contests.permissions.HasViewContestPermission,
            api.contests.permissions.HasViewScoreboardPermission,
        ),
        'get_ctftime_scoreboard': (
            api.contests.permissions.HasViewContestPermission,
            api.contests.permissions.HasViewScoreboardPermission,
        ),
    }

    def get_queryset(self):
        qs = super(ContestViewSet, self).get_queryset()

        if self.action == 'list':
            qs = qs.only_published()
            qs = qs.with_user_registered(self.request.user)

        if self.action in ['list', 'retrieve']:
            qs = qs.with_opened_at(self.request.user)

        return qs

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
            obj.can_view_scoreboard = obj.public_scoreboard or obj.can_edit_contest

            # if a user is registered & has opened contest, set open contest date
            if not obj.is_finished:
                team = obj.get_participating_team(self.request.user)
                cnt = api.models.ContestParticipantRelationship.objects.filter(
                    contest=obj,
                    participant=team,
                    opened_contest_at__isnull=True,
                ).update(opened_contest_at=timezone.now())
                if cnt:
                    obj.refresh_from_db()

        return obj

    def list(self, request, *args, **kwargs):
        all_contests = self.get_queryset()
        upcoming_queryset = all_contests.only_upcoming()
        running_queryset = all_contests.only_running()
        finished_queryset = all_contests.only_finished()

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
        serializer = self.get_serializer(instance=instance)
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

    def get_ordered_scoreboard_users_page(self, contest):
        relations_queryset = contest.get_scoreboard_relations_queryset()

        users_paginator = api.pagination.ScoreboardPagination()
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
        ).select_related(
            'participant',
        ).prefetch_related(
            'registered_users',
        ).order_by(
            '-id',
        )
        paginator = api.pagination.ContestRegistrationsPagination()
        page = paginator.paginate_queryset(queryset=queryset, request=self.request)
        serializer = api.contests.serializers.CPRSerializer(page, many=True)
        return Response(serializer.data)

    @cache_response(
        timeout=5,
        key_func=api.contests.caching.ScoreboardKeyConstructor(),
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
        timeout=60,
        key_func=api.contests.caching.ScoreboardKeyConstructor(),
    )
    @action(
        detail=True,
        url_path='ctftime_scoreboard',
        url_name='ctftime_scoreboard',
        methods=['get'],
    )
    def get_ctftime_scoreboard(self, _request, *_args, **_kwargs):
        contest = self.get_object()
        relations_queryset = contest.get_scoreboard_relations_queryset()

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
    filterset_fields = ('contest_id',)

    def get_queryset(self):
        qs = super(ContestParticipantRelationshipViewSet, self).get_queryset()
        if self.action == 'delete':
            qs = qs.select_related('contest')
        return qs.filter(participant__participants__id=self.request.user.id)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        contest = instance.contest
        if contest.is_running or contest.is_finished:
            raise ValidationError('Too late to unregister')
        return super(ContestParticipantRelationshipViewSet, self).destroy(request, *args, **kwargs)


class ContestTaskRelationshipViewSet(CustomPermissionsViewSetMixin,
                                     rest_mixins.CreateModelMixin,
                                     rest_mixins.UpdateModelMixin,
                                     rest_mixins.DestroyModelMixin,
                                     rest_viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = api.models.ContestTaskRelationship.objects.select_related(
        'main_tag',
    ).prefetch_related(
        'task__tags',
    )

    serializer_class = api.contests.serializers.CTRSerializer

    action_permission_classes = {
        'create': (api.contests.permissions.HasContestTaskRelationshipPermission,),
        'update': (api.contests.permissions.HasContestTaskRelationshipPermission,),
        'partial_update': (api.contests.permissions.HasContestTaskRelationshipPermission,),
        'destroy': (api.contests.permissions.HasContestTaskRelationshipPermission,),
    }

    @atomic
    def create(self, request, *args, **kwargs):
        return super(ContestTaskRelationshipViewSet, self).create(request, *args, **kwargs)

    def get_serializer(self, *args, **kwargs):
        if self.action == 'create':
            # noinspection PyUnresolvedReferences
            kwargs['many'] = isinstance(self.request.data, list)
        return super(ContestTaskRelationshipViewSet, self).get_serializer(*args, **kwargs)


class ContestTaskViewSet(rest_viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = api.contests.serializers.ContestTaskPreviewSerializer
    lookup_field = 'task_id'
    lookup_url_kwarg = 'task_id'
    queryset = api.models.Task.objects.all()

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
                raise PermissionDenied('No access.')

            if contest.is_upcoming:
                raise PermissionDenied('Contest is not started yet')

        team = contest.get_participating_team(self.request.user)
        if not can_view and not contest.is_finished and team is None:
            raise PermissionDenied('Register for a contest first')

        if self.action == 'retrieve' and not contest.is_finished and team:
            # if a user is registered & has opened contest, set open contest date
            api.models.ContestParticipantRelationship.objects.filter(
                contest=contest,
                participant=team,
                opened_contest_at__isnull=True,
            ).update(opened_contest_at=timezone.now())

        return contest

    @staticmethod
    def relation_to_task(relation):
        task = relation.task

        task.is_solved_by_user = relation.is_solved_by_user
        task.is_solved_on_upsolving = relation.is_solved_on_upsolving
        task.solved_count = relation.solved_count
        task.main_tag = relation.main_tag
        task.contest_cost = relation.current_cost

        return task

    def get_queryset(self):
        contest = self.get_contest()

        qs = api.models.ContestTaskRelationship.objects.all()
        qs = qs.with_solved_on_upsolving(self.request.user)
        qs = qs.with_solved_count()

        if contest.dynamic_scoring:
            qs = qs.with_dynamic_cost()
        else:
            qs = qs.with_static_cost()

        team = contest.get_participating_team(self.request.user)
        qs = qs.with_solved_by_team(team)

        qs = qs.filter(
            contest=contest,
        ).prefetch_related(
            'task__tags',
        ).select_related(
            'task',
            'task__author',
            'main_tag',
        )

        if self.action in ['retrieve', 'get_solved', 'submit_flag']:
            return qs

        tasks = list(map(self.relation_to_task, qs))

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
            qs = self.get_queryset()
            task = self.relation_to_task(qs.get(task_id=task_id))
        except api.models.ContestTaskRelationship.DoesNotExist:
            raise NotFound('No such task.')

        if self.action == 'retrieve':
            task.can_edit_task = self.request.user.has_perm('change_task', task)

        return task

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return api.contests.serializers.ContestTaskViewSerializer
        return super(ContestTaskViewSet, self).get_serializer_class()

    def retrieve(self, request, *args, **kwargs):
        return super(ContestTaskViewSet, self).retrieve(request, *args, **kwargs)

    @cache_response(timeout=5, key_func=api.contests.caching.ContestTaskListKeyConstructor())
    def list(self, request, *args, **kwargs):
        return super(ContestTaskViewSet, self).list(request, *args, **kwargs)

    @cache_response(timeout=30, key_func=api.contests.caching.ContestTaskSolvedKeyConstructor())
    @action(detail=True,
            url_name='solved',
            url_path='solved',
            methods=['get'])
    def get_solved(self, *_args, **_kwargs):
        task = self.get_object()
        contest = self.get_contest()

        if not contest.public_scoreboard and not self.request.user.has_perm('api.change_contest', contest):
            raise PermissionDenied('You don\'t have access to this page')

        solved_participants_queryset = api.models.ContestTaskRelationship.objects.get(
            task=task,
            contest=contest,
        ).solved_by.order_by('-id').all()

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
    @ratelimit(
        key=api.contests.permissions.get_submission_ratelimit_key,
        rate='4/m',
    )
    def submit_flag(self, *_args, **_kwargs):
        if getattr(self.request, 'limited', False):
            raise Throttled(detail='You can submit a flag 4 times per minute.')

        task = self.get_object()

        if self.request.user.has_perm('api.change_task', task):
            raise ValidationError({'flag': 'You cannot submit this task'})

        contest = self.get_contest()
        team = contest.get_participating_team(self.request.user)

        # One cannot submit the task during the contest without a registered team
        # to prevent abuse.
        if not team and contest.is_running:
            raise ValidationError({'flag': 'You are not registered for a contest'})

        relation = api.models.ContestTaskRelationship.objects.get(
            contest=contest,
            task=task,
        )

        if team and relation.solved_by.filter(id=team.id).exists():
            raise PermissionDenied('Task already solved.')

        # noinspection PyUnresolvedReferences
        serializer = api.tasks.serializers.TaskSubmitSerializer(
            data=self.request.data,
            instance=task,
        )

        submission = api.models.Submission(
            user=self.request.user,
            participant=team,
            contest=contest,
            task=task,
            flag=serializer.initial_data.get('flag'),
        )
        try:
            serializer.is_valid(raise_exception=True)
            submission.success = True
        except ValidationError:
            submission.success = False
            raise
        finally:
            submission.save()

        solved_at = timezone.now()
        user = self.request.user
        upsolving = True
        # If is registered and (if virtual) is participating virtually.
        if team and contest.is_running and (not contest.is_virtual or contest.is_virtually_running_for(user)):
            upsolving = False
            relation.solved_by.add(team)
            contest.contest_participant_relationship.filter(
                participant=team,
            ).update(
                last_solve=solved_at,
            )

        task.solved_by.add(user)
        self.request.user.last_solve = solved_at
        self.request.user.save(update_fields=['last_solve'])

        return Response(dict(success=True, upsolving=upsolving))
