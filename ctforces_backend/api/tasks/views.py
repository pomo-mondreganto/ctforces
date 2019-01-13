from django.db.models import Count, Exists, OuterRef
from django.utils import timezone
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
    queryset = api_models.Task.objects.order_by('-publication_time')

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

        if self.action == 'list':
            queryset = queryset.filter(is_published=True)

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
    def get_solved(self, _request, *_args, **_kwargs):
        instance = self.get_object()
        users_solved = instance.solved_by.all()
        paginator = api_pagination.UserDefaultPagination()
        page = paginator.paginate_queryset(
            queryset=users_solved,
            request=self.request,
        )

        if page is not None:
            serializer = api_users_serializers.UserBasicSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = api_users_serializers.UserBasicSerializer(users_solved, many=True)
        return Response(serializer.data)

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
