from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_GET
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from api import models as api_models
from api import serializers as api_serializers
from api.token_operations import serialize


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
            subject='Nimbel account confirmation',
            message=message_plain,
            from_email='Nimbel team',
            recipient_list=[user_email],
            html_message=message_html
        )
