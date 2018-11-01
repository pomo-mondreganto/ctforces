from django.conf import settings
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.http import require_GET
from rest_framework import mixins as rest_mixins
from rest_framework import viewsets as rest_viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api import models as api_models
from api import pagination as api_pagination
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


class UserViewSet(rest_mixins.RetrieveModelMixin,
                  rest_mixins.ListModelMixin,
                  rest_viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = api_serializers.UserBasicSerializer
    queryset = api_models.User.upsolving_annotated.all()
    pagination_class = api_pagination.UserTopPagination
    lookup_field = 'username'
    lookup_url_kwarg = 'username'

    @action(detail=False, url_name='upsolving_top', url_path='upsolving_top')
    def get_upsolving_top(self, _request):
        users_with_upsolving = self.get_queryset().only('username').order_by('-cost_sum', 'last_solve')
        page = self.paginate_queryset(users_with_upsolving)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(users_with_upsolving, many=True)
        return Response(serializer.data)

    @action(detail=False, url_name='rating_top', url_path='rating_top')
    def get_rating_top(self, _request):
        users_with_rating = api_models.User.objects.only('username', 'rating').order_by('-rating', 'last_solve')
        page = self.paginate_queryset(users_with_rating)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(users_with_rating, many=True)
        return Response(serializer.data)

    @action(detail=False, url_name='search', url_path='search')
    def search_users(self, request):
        username = request.query_params.get('username', '')
        users_list = api_models.User.objects.only('username').filter(username__istartswith=username)[:10]
        serializer = self.get_serializer(users_list, many=True)
        return Response(serializer.data)
