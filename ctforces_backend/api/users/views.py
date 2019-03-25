from django.conf import settings
from django.contrib.auth import authenticate, login, logout
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

from api import celery_tasks as api_tasks
from api import models as api_models
from api import pagination as api_pagination
from api.contests import serializers as api_contests_serializers
from api.posts import serializers as api_posts_serializers
from api.tasks import serializers as api_tasks_serializers
from api.token_operations import serialize, deserialize
from api.users import serializers as api_users_serializers


class UserCreateView(CreateAPIView):
    model = api_models.User
    serializer_class = api_users_serializers.UserCreateSerializer
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
            'email_url': settings.EMAIL_URL,
        }

        message_plain = render_to_string('email_templates/email_confirmation.txt', context)
        message_html = render_to_string('email_templates/email_confirmation.html', context)

        api_tasks.send_users_mail.delay(
            subject='CTForces account confirmation',
            message=message_plain,
            from_email='CTForces team',
            recipient_list=[user_email],
            html_message=message_html,
        )

        instance.last_email_resend = timezone.now()
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

        user = api_models.User.objects.filter(id=user_id).first()
        if not user:
            raise ValidationError('No such user.')
        user.is_active = True
        user.save()
        return Response(user_id)


class ActivationEmailResendView(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        email = request.data.get('email', '').lower()
        user = api_models.User.objects.filter(email=email).first()
        if not user:
            raise ValidationError('User with such email is not registered')
        if user.is_active:
            raise ValidationError('User is already activated')

        delta = timezone.now() - user.last_email_resend

        if delta < timezone.timedelta(hours=1):
            raise ValidationError(
                'You can resend activation email in {0} minutes {1} seconds'.format(
                    delta.seconds // 60,
                    delta.seconds % 60,
                )
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
            message=message_plain,
            from_email='CTForces team',
            recipient_list=[email],
            html_message=message_html,
        )

        user.last_email_resend = timezone.now()

        return Response('ok')


class PasswordResetRequestView(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        email = request.data.get('email', '').lower()
        user = api_models.User.objects.filter(email=email).first()
        if not user:
            raise ValidationError('User with such email is not registered')

        delta = timezone.now() - user.last_email_resend

        if delta < timezone.timedelta(hours=1):
            raise ValidationError(
                'You can resend password reset email in {0} minutes {1} seconds'.format(
                    delta.seconds // 60,
                    delta.seconds % 60,
                )
            )

        token = serialize(user.id, 'password_reset.txt')

        context = {
            'token': token,
            'username': user.username,
            'email_url': settings.EMAIL_URL,
        }

        message_plain = render_to_string('email_templates/password_reset.txt', context)
        message_html = render_to_string('email_templates/password_reset.html', context)

        api_tasks.send_users_mail.delay(
            subject='CTForces password reset',
            message=message_plain,
            from_email='CTForces team',
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
            raise ValidationError('Token is invalid or has expired.')

        user = api_models.User.objects.filter(id=user_id).first()
        if not user:
            raise ValidationError('No such user.')

        serializer = api_users_serializers.UserPasswordResetSerializer(data={'password': new_password}, instance=user)
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
        response_data = api_users_serializers.UserBasicSerializer(user).data
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
        serializer = api_users_serializers.AvatarUploadSerializer(data=request.data,
                                                                  instance=request.user,
                                                                  context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


class UserViewSet(rest_viewsets.ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = api_users_serializers.UserBasicSerializer
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
    def get_users_tasks(self, request, **_kwargs):
        tasks_type = request.query_params.get('type', 'all')
        user = self.get_object()
        queryset = api_models.Task.objects.filter(is_published=True, author=user)

        if tasks_type == 'all':
            queryset = (queryset | get_objects_for_user(request.user, 'view_task', api_models.Task)).distinct()

        queryset = queryset.order_by('-id')
        paginator = api_pagination.TaskDefaultPagination()
        page = paginator.paginate_queryset(
            queryset=queryset,
            request=self.request,
        )

        if page is not None:
            serializer = api_tasks_serializers.TaskPreviewSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = api_tasks_serializers.TaskPreviewSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, url_name='posts', url_path='posts', methods=['get'])
    def get_users_posts(self, request, **_kwargs):
        posts_type = request.query_params.get('type', 'all')
        user = self.get_object()
        queryset = api_models.Post.objects.filter(is_published=True, author=user)

        if posts_type == 'all':
            queryset = (queryset | get_objects_for_user(request.user, 'view_post', api_models.Post)).distinct()

        queryset = queryset.order_by('-id')
        paginator = api_pagination.PostDefaultPagination()
        page = paginator.paginate_queryset(
            queryset=queryset,
            request=self.request,
        )

        if page is not None:
            serializer = api_posts_serializers.PostMainSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = api_posts_serializers.PostMainSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, url_name='contests', url_path='contests', methods=['get'])
    def get_users_contests(self, request, **_kwargs):
        contests_type = request.query_params.get('type', 'all')
        user = self.get_object()
        queryset = api_models.Contest.objects.filter(is_published=True, author=user)

        if contests_type == 'all':
            queryset = (queryset | get_objects_for_user(request.user, 'view_contest', api_models.Contest)).distinct()

        queryset = queryset.order_by('-id')
        paginator = api_pagination.ContestDefaultPagination()
        page = paginator.paginate_queryset(
            queryset=queryset,
            request=self.request,
        )

        if page is not None:
            serializer = api_contests_serializers.ContestPreviewSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = api_contests_serializers.ContestPreviewSerializer(queryset, many=True)
        return Response(serializer.data)
