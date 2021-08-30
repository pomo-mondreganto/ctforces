from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.db.models import Exists, OuterRef
from django.db.transaction import atomic
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from guardian.shortcuts import get_objects_for_user
from rest_framework import viewsets as rest_viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_extensions.cache.decorators import cache_response

from api import celery_tasks as api_tasks
from api import models as api_models
from api import pagination as api_pagination
from api.posts import serializers as api_posts_serializers
from api.tasks import serializers as api_tasks_serializers
from api.teams import serializers as api_teams_serializers
from api.tokens import serialize, deserialize
from api.users import caching as api_users_caching
from api.users import filters as api_users_filters
from api.users import serializers as api_users_serializers


class UserCreateView(CreateAPIView):
    model = api_models.User
    serializer_class = api_users_serializers.UserCreateSerializer
    permission_classes = (AllowAny,)

    @staticmethod
    def send_confirmation(user):
        token = serialize(user.id, 'email_confirmation')

        context = {
            'token': token,
            'username': user.username,
            'email_url': settings.EMAIL_URL,
        }

        message_plain = render_to_string('email_templates/email_confirmation.txt', context)
        message_html = render_to_string('email_templates/email_confirmation.html', context)

        api_tasks.send_users_mail.delay(
            subject='CTForces account confirmation',
            text_message=message_plain,
            recipient_list=[user.email],
            html_message=message_html,
        )

        user.last_email_resend = timezone.now()
        user.save()

    @atomic
    def perform_create(self, serializer):
        instance = serializer.save()
        if settings.EMAIL_ENABLED:
            self.send_confirmation(instance)
        else:
            instance.is_active = True
            instance.save()


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
            raise ValidationError({'detail': 'Token is invalid or has expired.'})

        user = api_models.User.objects.filter(id=user_id).first()
        if not user:
            raise ValidationError({'detail': 'No such user.'})
        user.is_active = True
        user.save()
        return Response(user_id)


class ActivationEmailResendView(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        if not settings.EMAIL_ENABLED:
            raise ValidationError(detail='Functionality is disabled for this server')

        email = request.data.get('email', '').lower()
        user = api_models.User.objects.filter(email=email).first()
        if not user:
            raise ValidationError({'email': 'User with such email is not registered'})
        if user.is_active:
            raise ValidationError({'email': 'User is already activated'})

        last_resend = user.last_email_resend
        if not last_resend:
            last_resend = timezone.now() - timezone.timedelta(seconds=settings.EMAIL_RESEND_COOLDOWN + 1)
        delta = timezone.now() - last_resend

        if delta < timezone.timedelta(seconds=settings.EMAIL_RESEND_COOLDOWN):
            raise ValidationError(
                {
                    'detail':
                        'You can resend activation email in {0} minutes {1} seconds'.format(
                            delta.seconds // 60,
                            delta.seconds % 60,
                        )
                }
            )

        token = serialize(user.id, 'email_confirmation')

        context = {
            'token': token,
            'username': user.username,
            'email_url': settings.EMAIL_URL,
        }

        message_plain = render_to_string('email_templates/email_confirmation.txt', context)
        message_html = render_to_string('email_templates/email_confirmation.html', context)

        api_tasks.send_users_mail.delay(
            subject='CTForces account confirmation',
            text_message=message_plain,
            recipient_list=[email],
            html_message=message_html,
        )

        user.last_email_resend = timezone.now()

        return Response('ok')


class PasswordResetRequestView(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        if not settings.EMAIL_ENABLED:
            raise ValidationError(detail='Functionality is disabled for this server')

        email = request.data.get('email', '').lower()
        user = api_models.User.objects.filter(email=email).first()
        if not user:
            raise ValidationError({'email': 'User with such email is not registered'})

        last_resend = user.last_email_resend
        if not last_resend:
            last_resend = timezone.now() - timezone.timedelta(seconds=settings.EMAIL_RESEND_COOLDOWN + 1)
        delta = timezone.now() - last_resend

        if delta < timezone.timedelta(seconds=settings.EMAIL_RESEND_COOLDOWN):
            raise ValidationError(
                {
                    'detail':
                        'You can resend activation email in {0} minutes {1} seconds'.format(
                            delta.seconds // 60,
                            delta.seconds % 60,
                        )
                }
            )

        token = serialize(user.id, 'password_reset')

        context = {
            'token': token,
            'username': user.username,
            'email_url': settings.EMAIL_URL,
        }

        message_plain = render_to_string('email_templates/password_reset.txt', context)
        message_html = render_to_string('email_templates/password_reset.html', context)

        api_tasks.send_users_mail.delay(
            subject='CTForces password reset',
            text_message=message_plain,
            from_email='noreply@ctforces.com',
            recipient_list=[email],
            html_message=message_html,
        )

        user.last_email_resend = timezone.now()

        return Response('ok')


class PasswordResetEndpointView(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        token = request.data.get('token')
        new_password = request.data.get('password')
        user_id = deserialize(token, token_type='password_reset', max_age=86400)
        try:
            user_id = int(user_id)
            if not user_id:
                raise TypeError
        except TypeError:
            raise ValidationError({'detail': 'Token is invalid or has expired.'})

        user = api_models.User.objects.filter(id=user_id).first()
        if not user:
            raise ValidationError({'detail': 'No such user.'})

        serializer = api_users_serializers.UserPasswordResetSerializer(
            data={
                'password': new_password
            },
            instance=user,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

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

        if not user.is_active:
            raise AuthenticationFailed('User is not activated')

        login(request, user)
        response_data = api_users_serializers.UserBasicSerializer(
            user,
            context={'request': request},
        ).data
        return Response(response_data)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        logout(request)
        return Response('ok')


class CurrentUserRetrieveUpdateView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = api_users_serializers.UserMainSerializer

    def get_queryset(self):
        if self.request.method == 'GET':
            return api_models.User.upsolving_annotated.annotate(
                has_tasks=Exists(
                    api_models.Task.objects.filter(
                        author_id=OuterRef('id'),
                    ),
                ),
                has_contests=Exists(
                    api_models.Contest.objects.filter(
                        author_id=OuterRef('id'),
                    ),
                ),
                has_posts=Exists(
                    api_models.Post.objects.filter(
                        author_id=OuterRef('id'),
                    ),
                ),
            ).all()
        return api_models.User.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.request.user.id)

        if self.request.method == 'GET':
            obj.can_create_tasks = self.request.user.has_perm('api.add_task')
            obj.can_create_posts = True
            obj.can_create_contests = self.request.user.has_perm('api.add_contest')
            obj.can_create_taskfiles = self.request.user.has_perm('api.add_taskfile')
            obj.is_admin = self.request.user.is_admin

        return obj

    @cache_response(timeout=3600, key_func=api_users_caching.CurrentUserRetrieveKeyConstructor())
    def retrieve(self, request, *args, **kwargs):
        return super(CurrentUserRetrieveUpdateView, self).retrieve(request, *args, **kwargs)


class AvatarUploadView(APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        serializer = api_users_serializers.AvatarUploadSerializer(data=request.data,
                                                                  instance=request.user,
                                                                  context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserViewSet(rest_viewsets.ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = api_users_serializers.UserBasicSerializer
    queryset = api_models.User.upsolving_annotated.all()
    pagination_class = api_pagination.UserDefaultPagination
    lookup_field = 'username'
    lookup_url_kwarg = 'username'
    filterset_class = api_users_filters.UserFilter

    @action(detail=True, url_name='tasks', url_path='tasks', methods=['get'])
    def get_users_tasks(self, request, **_kwargs):
        tasks_type = request.query_params.get('type', 'all')
        user = self.get_object()
        qs = api_models.Task.objects.published()

        if tasks_type == 'all':
            qs = (qs | get_objects_for_user(request.user, 'view_task', api_models.Task)).distinct()

        qs = qs.filter(author=user).order_by('-id').prefetch_related('tags')
        qs = qs.with_solved_count().with_solved_by_user(self.request.user)

        return api_pagination.get_paginated_response(
            paginator=api_pagination.TaskDefaultPagination(),
            queryset=qs,
            serializer_class=api_tasks_serializers.TaskPreviewSerializer,
            request=request,
        )

    @action(detail=True, url_name='posts', url_path='posts', methods=['get'])
    def get_users_posts(self, request, **_kwargs):
        posts_type = request.query_params.get('type', 'all')
        user = self.get_object()
        queryset = api_models.Post.objects.filter(is_published=True)

        if posts_type == 'all':
            queryset = (queryset | get_objects_for_user(request.user, 'view_post', api_models.Post)).distinct()

        queryset = queryset.filter(author=user)
        queryset = queryset.order_by('-id').select_related('author')

        return api_pagination.get_paginated_response(
            paginator=api_pagination.PostDefaultPagination(),
            queryset=queryset,
            serializer_class=api_posts_serializers.PostMainSerializer,
            request=request,
        )

    @action(detail=True, url_name='teams', url_path='teams', methods=['get'])
    def get_users_teams(self, request, **_kwargs):
        user = self.get_object()
        queryset = user.teams.all()
        queryset = queryset.order_by('-id')

        return api_pagination.get_paginated_response(
            paginator=api_pagination.TeamDefaultPagination(),
            queryset=queryset,
            serializer_class=api_teams_serializers.TeamMinimalSerializer,
            request=request,
        )
