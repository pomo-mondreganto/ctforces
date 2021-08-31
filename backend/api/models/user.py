import re
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import (
    Sum,
    Value as V,
    Q,
)
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.utils.deconstruct import deconstructible
from django.utils.functional import cached_property
from rest_framework_tricks.models.fields import NestedProxyField
from stdimage.models import StdImageField

from api.storages import DefaultStorage
from .auxiliary import (
    CustomImageSizeValidator,
    CustomUploadTo,
    stdimage_processor,
)


@deconstructible
class ASCIIUsernameValidator(RegexValidator):
    regex = r'^[\w_-]{3,15}$'
    message = (
        'Username needs to contain from 3 to 15 English letters, '
        'numbers, and -/_ characters'
    )
    flags = re.ASCII


class UserQuerySet(models.QuerySet):
    def with_cost_sum(self):
        return self.annotate(
            cost_sum=Coalesce(
                Sum(
                    'solved_tasks__cost',
                    filter=Q(solved_tasks__show_on_main_page=True),
                ),
                V(0),
            ),
        )


class CustomUserManager(UserManager):
    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)


class User(AbstractUser):
    username_validator = ASCIIUsernameValidator()
    email = models.EmailField('email address', blank=False, unique=True, null=False)

    rating = models.IntegerField(default=2000)
    max_rating = models.IntegerField(default=2000)

    updated_at = models.DateTimeField(auto_now=True)
    last_solve = models.DateTimeField(default=timezone.now)

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
        storage=DefaultStorage(),
        default='avatars/default.png',
        null=False, blank=False,
    )

    objects = CustomUserManager()

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
