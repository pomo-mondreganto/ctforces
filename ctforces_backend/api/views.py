from django.conf import settings
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_GET
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
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


class UserRatingTopList(ListAPIView):
    permission_classes = (AllowAny,)
    pagination_class = api_pagination.UserTopPagination
    queryset = api_models.User.objects.only('username', 'rating').order_by('-rating')
    serializer_class = api_serializers.UserBasicSerializer


class GetCurrentUserView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = api_serializers.UserBasicSerializer

    def get_object(self):
        return self.request.user


class AvatarUploadView(APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        serializer = api_serializers.AvatarUploadSerializer(data=request.data, instance=request.user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
