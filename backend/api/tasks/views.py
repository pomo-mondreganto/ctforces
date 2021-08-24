from django.db.models import Count, Exists, OuterRef
from django.utils import timezone
from rest_framework import mixins as rest_mixins
from rest_framework import serializers as rest_serializers
from rest_framework import viewsets as rest_viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

import api.mixins
import api.models
import api.pagination
import api.tasks.filters
import api.tasks.permissions
import api.tasks.serializers
import api.users.serializers


class TaskViewSet(api.mixins.CustomPermissionsViewSetMixin,
                  rest_viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = api.pagination.TaskDefaultPagination
    filterset_class = api.tasks.filters.TaskFilterSet

    queryset = api.models.Task.objects.order_by(
        '-publication_time',
        '-id',
    ).select_related('author')

    action_permission_classes = {
        'retrieve': (api.tasks.permissions.HasViewTaskPermission,),
        'get_solved': (api.tasks.permissions.HasViewTaskPermission,),
        'get_full_task': (api.tasks.permissions.HasEditTaskPermission,),
        'create': (api.tasks.permissions.HasCreateTaskPermission,),
        'update': (api.tasks.permissions.HasEditTaskPermission,),
        'partial_update': (api.tasks.permissions.HasEditTaskPermission,),
        'destroy': (api.tasks.permissions.HasDeleteTaskPermission,),
    }

    def get_queryset(self):
        queryset = super(TaskViewSet, self).get_queryset()

        if self.action == 'get_solved':
            return queryset.prefetch_related('solved_by')

        queryset = queryset.prefetch_related('tags').select_related('author')

        if self.action == 'list':
            queryset = queryset.filter(show_on_main_page=True)

        if self.action in ['retrieve', 'get_full_task']:
            queryset = queryset.prefetch_related('files')

        return queryset.annotate(
            solved_count=Count(
                'solved_by',
                distinct=True,
            ),
            is_solved_by_user=Exists(
                api.models.Task.objects.filter(
                    id=OuterRef('id'),
                    solved_by=self.request.user.id or -1,
                )
            ),
        )

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return api.tasks.serializers.TaskViewSerializer
        if self.action == 'list':
            return api.tasks.serializers.TaskPreviewSerializer
        if self.action == 'get_full_task':
            return api.tasks.serializers.TaskFullSerializer
        return api.tasks.serializers.TaskFullSerializer

    def get_object(self):
        obj = super(TaskViewSet, self).get_object()
        if self.action == 'retrieve':
            obj.can_edit_task = self.request.user.has_perm('change_task', obj)
        return obj

    @action(
        detail=True,
        url_path='full',
        url_name='full',
        methods=['get'],
    )
    def get_full_task(self, request, *args, **kwargs):
        return super(TaskViewSet, self).retrieve(request, *args, **kwargs)

    @action(
        detail=True,
        url_path='solved',
        url_name='solved',
        methods=['get'],
    )
    def get_solved(self, request, *_args, **_kwargs):
        instance = self.get_object()
        users_solved = instance.solved_by.filter(show_in_ratings=True)

        return api.pagination.get_paginated_response(
            paginator=api.pagination.UserDefaultPagination(),
            queryset=users_solved,
            serializer_class=api.users.serializers.UserBasicSerializer,
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
            raise rest_serializers.ValidationError({'flag': 'You cannot submit this task'})

        # to avoid updating last_solve incorrectly later
        if instance.solved_by.filter(id=request.user.id).exists():
            raise rest_serializers.ValidationError({'flag': 'You already submitted this task'})

        serializer = api.tasks.serializers.TaskSubmitSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)

        instance.solved_by.add(request.user)
        request.user.last_solve = timezone.now()
        request.user.save(update_fields=['last_solve'])
        return Response('accepted!')


class TaskTagViewSet(rest_mixins.CreateModelMixin,
                     rest_mixins.ListModelMixin,
                     rest_viewsets.GenericViewSet):
    permission_classes = (api.tasks.permissions.HasEditTaskPermissionOrReadOnly,)
    serializer_class = api.tasks.serializers.TaskTagSerializer
    pagination_class = api.pagination.TaskTagDefaultPagination
    queryset = api.models.TaskTag.objects.all()
    filterset_class = api.tasks.filters.TaskTagFilterSet

    def get_serializer(self, *args, **kwargs):
        if self.action == 'create':
            kwargs['many'] = isinstance(self.request.data, list)
        return super(TaskTagViewSet, self).get_serializer(*args, **kwargs)


class TaskFileViewSet(rest_mixins.RetrieveModelMixin,
                      rest_mixins.ListModelMixin,
                      rest_mixins.CreateModelMixin,
                      rest_viewsets.GenericViewSet):
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated, api.tasks.permissions.HasCreateTaskFilePermissionOrReadOnly)
    serializer_class = api.tasks.serializers.TaskFileSerializer
    pagination_class = api.pagination.TaskFileDefaultPagination
    queryset = api.models.TaskFile.objects.all()

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user.id)


class TaskHintViewSet(api.mixins.CustomPermissionsViewSetMixin,
                      rest_viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = api.models.TaskHint.objects.select_related('author')
    serializer_class = api.tasks.serializers.TaskHintSerializer

    action_permission_classes = {
        'retrieve': (api.tasks.permissions.HasViewTaskHintPermission,),
        'update': (api.tasks.permissions.HasEditTaskHintsPermission,),
        'partial_update': (api.tasks.permissions.HasEditTaskHintsPermission,),
        'destroy': (api.tasks.permissions.HasEditTaskHintsPermission,)
    }

    def get_queryset(self):
        qs = super(TaskHintViewSet, self).get_queryset()
        if self.action == 'list':
            qs = qs.filter(is_published=True)
        return qs
