from django.db.models import Count, Exists, OuterRef, Q
from django.utils import timezone
from django_filters import rest_framework as filters
from guardian.shortcuts import get_objects_for_user
from rest_framework import mixins as rest_mixins
from rest_framework import serializers as rest_serializers
from rest_framework import viewsets as rest_viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from api import mixins as api_mixins
from api import models as api_models
from api import pagination as api_pagination
from api.tasks import filters as api_tasks_filters
from api.tasks import permissions as api_tasks_permissions
from api.tasks import serializers as api_tasks_serializers
from api.users import serializers as api_users_serializers


class TaskViewSet(api_mixins.CustomPermissionsViewSetMixin,
                  api_mixins.CustomPermissionsQuerysetViewSetMixin,
                  rest_viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = api_pagination.TaskDefaultPagination
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    queryset = api_models.Task.objects.order_by('-publication_time', '-id').select_related('author')

    action_permission_classes = {
        'retrieve': (api_tasks_permissions.HasViewTaskPermission,),
        'get_solved': (api_tasks_permissions.HasViewTaskPermission,),
        'get_full_task': (api_tasks_permissions.HasEditTaskPermission,),
        'create': (api_tasks_permissions.HasCreateTaskPermission,),
        'update': (api_tasks_permissions.HasEditTaskPermission,),
        'partial_update': (api_tasks_permissions.HasEditTaskPermission,),
        'destroy': (api_tasks_permissions.HasDeleteTaskPermission,),
    }

    klass = api_models.Task
    action_permissions_querysets = {
        'update': 'change_task',
        'partial_update': 'change_task',
        'destroy': 'delete_task',
    }

    def get_queryset(self):
        queryset = super(TaskViewSet, self).get_queryset()
        queryset = queryset.prefetch_related('tags').select_related('author')

        if self.action == 'list' or self.action == 'search_task':
            queryset = queryset.filter(show_on_main_page=True)

        if self.action == 'retrieve' or self.action == 'get_full_task':
            queryset = queryset.prefetch_related('files')

        return queryset.annotate(
            solved_count=Count(
                'solved_by',
                distinct=True,
            ),
            is_solved_by_user=Exists(
                api_models.Task.objects.filter(
                    id=OuterRef('id'),
                    solved_by__id=self.request.user.id or -1,
                )
            ),
        )

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return api_tasks_serializers.TaskViewSerializer
        elif self.action == 'list':
            return api_tasks_serializers.TaskPreviewSerializer
        return api_tasks_serializers.TaskFullSerializer

    def get_object(self):
        obj = super(TaskViewSet, self).get_object()
        if self.action == 'retrieve':
            obj.can_edit_task = self.request.user.has_perm('change_task', obj)
        return obj

    @action(
        detail=False,
        url_path='search',
        url_name='search',
        methods=['get']
    )
    def search_task(self, request, *_args, **_kwargs):
        search_q = request.query_params.get('q', '')
        tasks = self.get_queryset().filter(
            Q(tags__name__icontains=search_q) |
            Q(name__icontains=search_q) |
            Q(author__username__icontains=search_q)
        )

        return api_pagination.get_paginated_response(
            paginator=api_pagination.TaskDefaultPagination(),
            queryset=tasks,
            serializer_class=api_tasks_serializers.TaskPreviewSerializer,
            request=request,
        )

    @action(
        detail=True,
        url_path='full',
        url_name='full',
        methods=['get'],
    )
    def get_full_task(self, _request, *_args, **_kwargs):
        instance = self.get_object()
        serializer = api_tasks_serializers.TaskFullSerializer(instance=instance)
        return Response(serializer.data)

    @action(
        detail=True,
        url_path='solved',
        url_name='solved',
        methods=['get'],
    )
    def get_solved(self, request, *_args, **_kwargs):
        instance = self.get_object()
        users_solved = instance.solved_by.filter(
            show_in_ratings=True,
        ).all()

        return api_pagination.get_paginated_response(
            paginator=api_pagination.UserDefaultPagination(),
            queryset=users_solved,
            serializer_class=api_users_serializers.UserBasicSerializer,
            request=request,
        )

    @action(
        detail=True,
        url_path='submit',
        url_name='submit',
        methods=['post'],
    )
    def submit(self, request, *_args, **_kwargs):
        instance = self.get_object()
        if self.request.user.has_perm('api.change_task', instance):
            raise rest_serializers.ValidationError(
                {
                    'flag': 'You cannot submit this task',
                },
            )

        # to avoid updating last_solve incorrectly later
        if instance.solved_by.filter(id=request.user.id).exists():
            raise rest_serializers.ValidationError(
                {
                    'flag': 'You already submitted this task',
                },
            )

        serializer = api_tasks_serializers.TaskSubmitSerializer(data=request.data, instance=instance)

        if serializer.is_valid(raise_exception=True):
            instance.solved_by.add(request.user)
            request.user.last_solve = timezone.now()
            request.user.save()
            return Response({'accepted!'})


class TaskTagViewSet(rest_mixins.CreateModelMixin,
                     rest_mixins.ListModelMixin,
                     rest_viewsets.GenericViewSet):
    permission_classes = (api_tasks_permissions.HasEditTaskPermissionOrReadOnly,)
    serializer_class = api_tasks_serializers.TaskTagSerializer
    pagination_class = api_pagination.TaskTagDefaultPagination
    queryset = api_models.TaskTag.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = api_tasks_filters.TaskTagFilter

    def get_serializer(self, *args, **kwargs):
        if self.action == 'create':
            kwargs['many'] = isinstance(self.request.data, list)
        return super(TaskTagViewSet, self).get_serializer(*args, **kwargs)


class TaskFileViewSet(rest_mixins.RetrieveModelMixin,
                      rest_mixins.ListModelMixin,
                      rest_mixins.CreateModelMixin,
                      rest_viewsets.GenericViewSet):
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated, api_tasks_permissions.HasCreateTaskFilePermissionOrReadOnly)
    serializer_class = api_tasks_serializers.TaskFileMainSerializer
    pagination_class = api_pagination.TaskFileDefaultPagination
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    queryset = api_models.TaskFile.objects.all()

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user.id)


class TaskHintViewSet(api_mixins.CustomPermissionsViewSetMixin,
                      rest_viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    queryset = api_models.TaskHint.objects.all().select_related('author')
    serializer_class = api_tasks_serializers.TaskHintSerializer

    action_permission_classes = {
        'retrieve': (api_tasks_permissions.HasViewTaskHintPermission,),
        'update': (api_tasks_permissions.HasModifyTaskHintsPermission,),
        'partial_update': (api_tasks_permissions.HasModifyTaskHintsPermission,),
        'destroy': (api_tasks_permissions.HasModifyTaskHintsPermission,)
    }

    def get_queryset(self):
        qs = super(TaskHintViewSet, self).get_queryset()
        if self.action == 'list':
            hints_type = self.request.query_params.get('type', 'published')

            if hints_type == 'published':
                qs = qs.filter(is_published=True)
            else:
                qs = get_objects_for_user(self.request.user, 'view_taskhint', api_models.TaskHint)

        return qs
