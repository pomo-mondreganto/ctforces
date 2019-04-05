from django.db.models import Count, Exists, OuterRef
from django.utils import timezone
from guardian.shortcuts import get_objects_for_user
from rest_framework import mixins as rest_mixins
from rest_framework import viewsets as rest_viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from api import mixins as api_mixins
from api import models as api_models
from api import pagination as api_pagination
from api import permissions as api_permissions
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
        'retrieve': (api_permissions.HasViewTaskPermission,),
        'get_full_task': (api_permissions.HasEditTaskPermission,),
        'create': (api_permissions.HasCreateTaskPermission,),
        'update': (api_permissions.HasEditTaskPermission,),
        'partial_update': (api_permissions.HasEditTaskPermission,),
        'destroy': (api_permissions.HasDeleteTaskPermission,),
    }

    klass = api_models.Task
    action_permissions_querysets = {
        'update': 'change_task',
        'partial_update': 'change_task',
        'destroy': 'delete_task',
    }

    def get_queryset(self):
        queryset = super(TaskViewSet, self).get_queryset()

        if self.action == 'list' or self.action == 'search_by_tag':
            queryset = queryset.filter(show_on_main_page=True)

        return queryset.annotate(
            solved_count=Count(
                'solved_by',
                distinct=True,
            ),
            is_solved_by_user=Exists(
                api_models.Task.objects.filter(
                    id=OuterRef('id'),
                    solved_by=self.request.user.id,
                )
            ),
        ).prefetch_related('tags', 'files')

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
        url_path='search_tag',
        url_name='search_tag',
        methods=['get']
    )
    def search_by_tag(self, request, *_args, **_kwargs):
        tag_name = request.query_params.get('name', '')
        tasks = self.get_queryset().filter(tags__name=tag_name)

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
        serializer = api_tasks_serializers.TaskSubmitSerializer(data=request.data, instance=instance)

        if serializer.is_valid(raise_exception=True):
            instance.solved_by.add(request.user)
            request.user.last_solve = timezone.now()
            request.user.save()
            return Response({'accepted!'})


class TaskTagViewSet(rest_mixins.CreateModelMixin,
                     rest_viewsets.GenericViewSet):
    permission_classes = (api_permissions.HasEditTaskPermissionOrReadOnly,)
    serializer_class = api_tasks_serializers.TaskTagSerializer
    queryset = api_models.TaskTag.objects.all()

    def get_serializer(self, *args, **kwargs):
        if self.action == 'create':
            kwargs['many'] = isinstance(self.request.data, list)
        return super(TaskTagViewSet, self).get_serializer(*args, **kwargs)

    @action(detail=False, url_name='search', url_path='search')
    def search_tags(self, request):
        tag_name = request.query_params.get('name', '')
        tag_list = self.get_queryset().only('name').filter(name__istartswith=tag_name)[:10]
        serializer = self.get_serializer(tag_list, many=True)
        return Response(serializer.data)


class TaskFileViewSet(rest_mixins.RetrieveModelMixin,
                      rest_mixins.ListModelMixin,
                      rest_mixins.CreateModelMixin,
                      rest_viewsets.GenericViewSet):
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated, api_permissions.HasCreateTaskFilePermissionOrReadOnly)
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
        'retrieve': (api_permissions.HasViewTaskHintPermission,),
        'update': (api_permissions.HasModifyTaskHintsPermission,),
        'partial_update': (api_permissions.HasModifyTaskHintsPermission,),
        'destroy': (api_permissions.HasModifyTaskHintsPermission,)
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
