import secrets

from celery import current_app
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from rest_framework_tricks.models.fields import NestedProxyField
from stdimage.models import StdImageField

from api import celery_tasks
from .auxiliary import (
    CustomImageSizeValidator,
    CustomUploadTo,
    stdimage_processor,
    CustomFileField,
    CustomASCIIUsernameValidator,
    TagNameValidator,
    UserUpsolvingAnnotatedManager,
    TeamRatingAnnotatedManager,
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


class Team(models.Model):
    name = models.CharField(max_length=25, null=False, blank=False, unique=True)
    join_token = models.CharField(max_length=255, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    captain = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        related_name='teams_captain',
        null=True, blank=True,
    )

    participants = models.ManyToManyField(
        'User',
        related_name='teams',
        blank=True,
    )

    objects = models.Manager()
    rating_annotated = TeamRatingAnnotatedManager()

    @staticmethod
    def gen_join_token(name):
        return f'{name}:{secrets.token_hex(16)}'

    class Meta:
        ordering = ('id',)
        permissions = (
            ('register_team', 'Can register teams for a contest'),
        )

        default_manager_name = 'objects'


class Post(models.Model):
    author = models.ForeignKey('User', on_delete=models.SET_NULL, related_name='posts', null=True, blank=True)
    title = models.CharField(max_length=200, blank=False)
    body = models.TextField(blank=False)
    is_published = models.BooleanField(default=False)
    show_on_main_page = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = (
            '-created_at',
            '-id',
        )


class TaskTag(models.Model):
    name = models.CharField(
        max_length=15,
        unique=True,
        validators=[TagNameValidator],
    )

    def __str__(self):
        return f"Tag {self.name} ({self.id})"

    class Meta:
        ordering = ('name',)


class Task(models.Model):
    author = models.ForeignKey('User', on_delete=models.SET_NULL, related_name='authored_tasks', null=True, blank=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(blank=True, null=False)

    flag = models.CharField(max_length=100, null=False, blank=False)

    solved_by = models.ManyToManyField('User', related_name='solved_tasks', blank=True)

    cost = models.IntegerField(null=False, blank=False, default=50)

    is_published = models.BooleanField(default=False)

    show_on_main_page = models.BooleanField(default=False)
    publication_time = models.DateTimeField(null=True, blank=True)

    tags = models.ManyToManyField('TaskTag', related_name='tasks', blank=True)

    uses_external_container = models.BooleanField(default=False)
    external_container_name = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(
        max_length=2,
        choices=(
            ('UP', 'Up & running'),
            ('DN', 'Down'),
        ),
        default='DN',
    )

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.is_published and self.publication_time is None:
            self.publication_time = timezone.now()
        elif not self.is_published and self.publication_time is not None:
            self.publication_time = None

        super(Task, self).save(force_insert=force_insert, force_update=force_update, using=using,
                               update_fields=update_fields)

    def __str__(self):
        return f"Task object ({self.id}:{self.name})"

    class Meta:
        ordering = ('id',)


class TaskHint(models.Model):
    author = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        related_name='authored_hints',
        null=True, blank=True
    )
    task = models.ForeignKey(
        'Task',
        on_delete=models.CASCADE,
        related_name='hints',
        null=False, blank=False
    )

    is_published = models.BooleanField(default=False)

    body = models.TextField(null=False, blank=True)

    def __str__(self):
        return f"TaskHint object ({self.id}), task {self.task_id}"


class TaskFile(models.Model):
    owner = models.ForeignKey('User', on_delete=models.SET_NULL, related_name='files', null=True, blank=True)
    task = models.ForeignKey('Task', on_delete=models.SET_NULL, related_name='files', null=True, blank=True)

    name = models.CharField(max_length=100, null=False, blank=False)

    upload_time = models.DateTimeField(auto_now_add=True)

    file_field = CustomFileField(
        upload_to=CustomUploadTo(
            upload_type='files',
            path='',
            append_random=True),
        blank=False, null=False
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return f"TaskFile object ({self.id}) for task {self.task_id}"


class Contest(models.Model):
    author = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        related_name='contests_authored',
        null=True, blank=True
    )

    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField()

    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    is_published = models.BooleanField(default=False)
    is_running = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)
    is_registration_open = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    publish_tasks_after_finished = models.BooleanField(default=True)
    is_rated = models.BooleanField(default=True)
    always_recalculate_rating = models.BooleanField(default=False)
    dynamic_scoring = models.BooleanField(default=False)

    celery_start_task_id = models.CharField(max_length=50, null=True, blank=True)
    celery_end_task_id = models.CharField(max_length=50, null=True, blank=True)

    tasks = models.ManyToManyField(
        'Task',
        related_name='contests',
        through='ContestTaskRelationship',
        blank=True
    )

    participants = models.ManyToManyField(
        'Team',
        related_name='contests_participated',
        through='ContestParticipantRelationship',
        blank=True,
    )

    def reset_start_action(self):
        if self.celery_start_task_id:
            current_app.control.revoke(self.celery_start_task_id)
        result = celery_tasks.start_contest.apply_async(args=(self.id,), eta=self.start_time)
        self.celery_start_task_id = result.id

    def reset_end_action(self):
        if self.celery_end_task_id:
            current_app.control.revoke(self.celery_end_task_id)
        result = celery_tasks.end_contest.apply_async(args=(self.id,), eta=self.end_time)
        self.celery_end_task_id = result.id

    def save(self, *args, **kwargs):
        if not self.id or Contest.objects.only('start_time').get(id=self.id).start_time != self.start_time:
            self.reset_start_action()

        if not self.id or Contest.objects.only('end_time').get(id=self.id).end_time != self.end_time:
            self.reset_end_action()

        super(Contest, self).save(*args, **kwargs)

    def __str__(self):
        return f"Contest object ({self.id}:{self.name})"
