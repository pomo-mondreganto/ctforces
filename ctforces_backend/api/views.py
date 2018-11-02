from django.conf import settings
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.decorators.http import require_GET
from guardian.shortcuts import get_objects_for_user
from rest_framework import mixins as rest_mixins
from rest_framework import status as rest_status
from rest_framework import viewsets as rest_viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from api import mixins as api_mixins
from api import models as api_models
from api import pagination as api_pagination
from api import permissions as api_permissions
from api import serializers as api_serializers
from api.token_operations import serialize, deserialize


@require_GET
def test_view(request):
    return HttpResponse('This is a test view')


class UserCreateView(CreateAPIView):
    model = api_models.User
    serializer_class = api_serializers.UserCreateSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        instance = serializer.save()
        user_id = instance.id
        user_username = instance.username
        user_email = instance.email
        token = serialize(user_id, 'email_confirmation')

        context = {
            'token': token,
            'username': user_username,
            'email_url': settings.EMAIL_URL
        }

        message_plain = render_to_string('email_templates/email_confirmation.txt', context)
        message_html = render_to_string('email_templates/email_confirmation.html', context)

        send_mail(
            subject='CTForces account confirmation',
            message=message_plain,
            from_email='CTForces team',
            recipient_list=[user_email],
            html_message=message_html
        )


class EmailConfirmationEndpointView(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        token = request.data.get('token')
        user_id = deserialize(token, token_type='email_confirmation', max_age=86400)
        try:
            user_id = int(user_id)
            if not user_id:
                raise TypeError
        except TypeError:
            raise ValidationError('Token is invalid or has expired.')

        user = api_models.User.objects.filter(id=user_id).first()
        if not user:
            raise ValidationError('No such user.')
        user.is_active = True
        user.save()
        return Response(user_id)


class LoginView(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials.')

        login(request, user)
        response_data = api_serializers.UserBasicSerializer(user).data
        return Response(response_data)


class CurrentUserRetrieveUpdateView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = api_serializers.UserMainSerializer

    def get_queryset(self):
        if self.request.method == 'GET':
            return api_models.User.upsolving_annotated.all()
        return api_models.User.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.request.user.id)
        return obj


class AvatarUploadView(APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        serializer = api_serializers.AvatarUploadSerializer(data=request.data, instance=request.user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


class UserViewSet(rest_viewsets.ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = api_serializers.UserBasicSerializer
    queryset = api_models.User.upsolving_annotated.all()
    pagination_class = api_pagination.UserDefaultPagination
    lookup_field = 'username'
    lookup_url_kwarg = 'username'

    @action(detail=False, url_name='upsolving_top', url_path='upsolving_top', methods=['get'])
    def get_upsolving_top(self, _request):
        users_with_upsolving = self.get_queryset().only('username').order_by('-cost_sum', 'last_solve')
        page = self.paginate_queryset(users_with_upsolving)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(users_with_upsolving, many=True)
        return Response(serializer.data)

    @action(detail=False, url_name='rating_top', url_path='rating_top', methods=['get'])
    def get_rating_top(self, _request):
        users_with_rating = api_models.User.objects.only('username', 'rating').order_by('-rating', 'last_solve')
        page = self.paginate_queryset(users_with_rating)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(users_with_rating, many=True)
        return Response(serializer.data)

    @action(detail=False, url_name='search', url_path='search', methods=['get'])
    def search_users(self, request):
        username = request.query_params.get('username', '')
        users_list = api_models.User.objects.only('username').filter(username__istartswith=username)[:10]
        serializer = self.get_serializer(users_list, many=True)
        return Response(serializer.data)

    @action(detail=True, url_name='tasks', url_path='tasks', methods=['get'])
    def get_users_tasks(self, request):
        tasks_type = request.query_params.get('type', 'published')
        user = self.get_object()
        if tasks_type == 'published':
            queryset = api_models.Task.objects.filter(is_published=True)
        else:
            queryset = get_objects_for_user(request.user, 'view_task')

        queryset = queryset.filter(author=user)
        paginator = api_pagination.UserDefaultPagination()
        page = paginator.paginate_queryset(
            queryset=queryset,
            request=self.request,
        )

        if page is not None:
            serializer = api_serializers.TaskPreviewSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = api_serializers.TaskPreviewSerializer(queryset, many=True)
        return Response(serializer.data)


class TaskViewSet(api_mixins.CustomPermissionsViewSetMixin, rest_viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    queryset = api_models.Task.objects.filter(is_published=True).annotate(
        solved_count=Count('solved_by')
    ).prefetch_related('tags')

    pagination_class = api_pagination.TaskDefaultPagination
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    action_permission_classes = {
        'get_full_task': (api_permissions.HasEditTaskPermission,),
        'create': (api_permissions.HasCreateTaskPermission,),
        'update': (api_permissions.HasEditTaskPermission,),
        'partial_update': (api_permissions.HasEditTaskPermission,),
        'destroy': (api_permissions.HasDeleteTaskPermission,),
    }

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return api_serializers.TaskViewSerializer
        elif self.action == 'list':
            return api_serializers.TaskPreviewSerializer
        return api_serializers.TaskFullSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.can_edit_task = request.user.has_perm('edit_task')
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(
        detail=True,
        url_path='full',
        url_name='full',
        methods=['get'],
    )
    def get_full_task(self, _request, *_args, **_kwargs):
        instance = self.get_object()
        print(_request.user.has_perm('edit_task', instance))
        serializer = api_serializers.TaskFullSerializer(instance=instance)
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
            serializer = api_serializers.UserBasicSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = api_serializers.UserBasicSerializer(users_solved, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        url_path='submit',
        url_name='submit',
        methods=['post'],
    )
    def submit(self, request, *_args, **_kwargs):
        instance = self.get_object()
        serializer = api_serializers.TaskSubmitSerializer(data=request.data, instance=instance)

        if serializer.is_valid(raise_exception=True):
            instance.solved_by.add(request.user)
            request.user.last_solve = timezone.now()
            request.user.save()
            return Response({'accepted!'})


class TaskTagViewSet(rest_mixins.CreateModelMixin,
                     rest_viewsets.GenericViewSet):
    permission_classes = (api_permissions.HasEditTaskPermissionOrReadOnly,)
    serializer_class = api_serializers.TaskTagSerializer
    queryset = api_models.TaskTag.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=rest_status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, url_name='search', url_path='search')
    def search_tags(self, request):
        tag_name = request.query_params.get('name', '')
        tag_list = self.get_queryset().only('name').filter(name__istartswith=tag_name)[:10]
        serializer = self.get_serializer(tag_list, many=True)
        return Response(serializer.data)
