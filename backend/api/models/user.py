from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from rest_framework_tricks.models.fields import NestedProxyField
from stdimage.models import StdImageField

from .auxiliary import (
    CustomImageSizeValidator,
    CustomUploadTo,
    stdimage_processor,
    CustomASCIIUsernameValidator,
    UserUpsolvingAnnotatedManager,
)


class User(AbstractUser):
    username_validator = CustomASCIIUsernameValidator()
    email = models.EmailField('email address', blank=False, unique=True, null=False)

    rating = models.IntegerField(default=2000)
    max_rating = models.IntegerField(default=2000)

    updated_at = models.DateTimeField(auto_now=True)
    last_solve = models.DateTimeField(default=timezone.now)

    has_participated_in_rated_contest = models.BooleanField(default=False)
    show_in_ratings = models.BooleanField(default=True)
    last_email_resend = models.DateTimeField(null=True, blank=True)

    avatar = StdImageField(
        variations={
            'main': (500, 500),
            'small': (150, 150)
        },
        upload_to=CustomUploadTo(
            upload_type='avatars',
            path='',
            random_filename=True,
        ),
        validators=[
            CustomImageSizeValidator(
                ratio=2,
                min_limit=(150, 150),
                max_limit=(1500, 1500),
            ),
        ],
        render_variations=stdimage_processor,
        default='avatars/default_avatar.png',
        blank=False, null=False
    )

    upsolving_annotated = UserUpsolvingAnnotatedManager()

    telegram = models.CharField(max_length=255, blank=True, null=False, default="")
    hide_personal_info = models.BooleanField(default=False)
    personal_info = NestedProxyField(
        'first_name',
        'last_name',
        'telegram',
    )

    @cached_property
    def is_admin(self):
        return self.is_superuser or self.groups.filter(name=settings.ADMIN_GROUP_NAME).exists()

    class Meta:
        ordering = ('id',)
        permissions = (
            ('view_personal_info', 'Can view user\'s personal information'),
        )

        default_manager_name = 'objects'
