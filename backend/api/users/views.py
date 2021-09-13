from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.db.transaction import atomic
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from rest_framework import viewsets as rest_viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_extensions.cache.decorators import cache_response

import api.models
import api.pagination
import api.posts.serializers
import api.tasks
import api.tasks.serializers
import api.teams.serializers
import api.users.caching
import api.users.filters
import api.users.serializers
from api.celery_tasks import send_email
from api.tokens import serialize, deserialize


class UserCreateView(CreateAPIView):
    model = api.models.User
    serializer_class = api.users.serializers.UserCreateSerializer
    permission_classes = (AllowAny,)

    @staticmethod
    def send_confirmation(user):
        token = serialize(user.id, 'email_confirmation')

        context = {
            'token': token,
            'username': user.username,
            'url': settings.EMAIL_URL,
            'logo': settings.LOGO_LINK,
        }

        message_plain = render_to_string('email_templates/email_confirmation.txt', context)
        message_html = render_to_string('email_templates/email_confirmation.html', context)

        send_email.delay(
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
            raise ValidationError('Token is invalid or has expired.')

        user = api.models.User.objects.filter(id=user_id).first()
        if not user:
            raise ValidationError('No such user.')
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
        user = api.models.User.objects.filter(email=email).first()
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
            'url': settings.EMAIL_URL,
            'logo': settings.LOGO_LINK,
        }

        message_plain = render_to_string('email_templates/email_confirmation.txt', context)
        message_html = render_to_string('email_templates/email_confirmation.html', context)

        send_email.delay(
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
        user = api.models.User.objects.filter(email=email).first()
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
            'url': settings.EMAIL_URL,
            'logo': settings.LOGO_LINK,
        }

        message_plain = render_to_string('email_templates/password_reset.txt', context)
        message_html = render_to_string('email_templates/password_reset.html', context)

        send_email.delay(
            subject='CTForces password reset',
            text_message=message_plain,
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

        user = api.models.User.objects.filter(id=user_id).first()
        if not user:
            raise ValidationError({'detail': 'No such user.'})

        serializer = api.users.serializers.UserPasswordResetSerializer(
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
        response_data = api.users.serializers.UserBasicSerializer(
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
    queryset = api.models.User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = api.users.serializers.UserMainSerializer

    def get_queryset(self):
        qs = super(CurrentUserRetrieveUpdateView, self).get_queryset()
        if self.request.method == 'GET':
            qs = qs.with_cost_sum()
        return qs

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.request.user.id)

        if self.request.method == 'GET':
            obj.can_create_tasks = self.request.user.has_perm('api.add_task')
            obj.can_create_contests = self.request.user.has_perm('api.add_contest')
            obj.is_admin = self.request.user.is_admin

        return obj

    @cache_response(timeout=3600, key_func=api.users.caching.CurrentUserRetrieveKeyConstructor())
    def retrieve(self, request, *args, **kwargs):
        return super(CurrentUserRetrieveUpdateView, self).retrieve(request, *args, **kwargs)


class AvatarUploadView(APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        serializer = api.users.serializers.AvatarUploadSerializer(data=request.data,
                                                                  instance=request.user,
                                                                  context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserViewSet(rest_viewsets.ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = api.users.serializers.UserBasicSerializer
    queryset = api.models.User.objects.all().with_cost_sum()
    pagination_class = api.pagination.UserDefaultPagination
    lookup_field = 'username'
    lookup_url_kwarg = 'username'
    filterset_class = api.users.filters.UserFilter

    @cache_response(timeout=5, key_func=api.users.caching.UserListKeyConstructor())
    def list(self, request, *args, **kwargs):
        return super(UserViewSet, self).list(request, *args, **kwargs)

    @action(detail=True, url_name='tasks', url_path='tasks', methods=['get'])
    def get_users_tasks(self, request, **_kwargs):
        user = self.get_object()
        qs = api.models.Task.objects.filter(author=user).order_by('-id').prefetch_related('tags')
        qs = qs.with_solved_count().with_solved_by_user(self.request.user)
        if user != self.request.user:
            qs = qs.published()

        return api.pagination.get_paginated_response(
            paginator=api.pagination.TaskDefaultPagination(),
            queryset=qs,
            serializer_class=api.tasks.serializers.TaskPreviewSerializer,
            request=request,
        )

    @action(detail=True, url_name='posts', url_path='posts', methods=['get'])
    def get_users_posts(self, request, **_kwargs):
        user = self.get_object()
        qs = api.models.Post.objects.filter(author=user).order_by('-id').select_related('author')
        if user != self.request.user:
            qs = qs.filter(is_published=True)

        return api.pagination.get_paginated_response(
            paginator=api.pagination.PostDefaultPagination(),
            queryset=qs,
            serializer_class=api.posts.serializers.PostMainSerializer,
            request=request,
        )

    @action(detail=True, url_name='teams', url_path='teams', methods=['get'])
    def get_users_teams(self, request, **_kwargs):
        user = self.get_object()
        queryset = user.teams.all()
        queryset = queryset.order_by('-id')

        return api.pagination.get_paginated_response(
            paginator=api.pagination.TeamDefaultPagination(),
            queryset=queryset,
            serializer_class=api.teams.serializers.TeamMinimalSerializer,
            request=request,
        )
