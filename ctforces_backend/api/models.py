from celery import current_app
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.db import models
from django.db.models import Sum, Q, Value as V
from django.db.models.functions import Coalesce
from django.utils import timezone
from rest_framework_tricks.models.fields import NestedProxyField
from stdimage.models import StdImageField

from api import celery_tasks
from api.models_auxiliary import CustomImageSizeValidator, CustomUploadTo, stdimage_processor, CustomFileField


class UserUpsolvingAnnotatedManager(UserManager):
    def get_queryset(self):
        return super(UserUpsolvingAnnotatedManager, self).get_queryset().annotate(
            cost_sum=Coalesce(
                Sum(
                    'solved_tasks__cost',
                    filter=Q(solved_tasks__is_published=True),
                ),
                V(0),
            )
        )


class User(AbstractUser):
    username_validator = ASCIIUsernameValidator()
    email = models.EmailField('email address', blank=False, unique=True, null=False)

    rating = models.IntegerField(default=2000)
    max_rating = models.IntegerField(default=2000)

    updated_at = models.DateTimeField(auto_now=True)

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

    last_solve = models.DateTimeField(default=timezone.now)

    upsolving_annotated = UserUpsolvingAnnotatedManager()

    hide_personal_info = models.BooleanField(default=False)

    personal_info = NestedProxyField(
        'first_name',
        'last_name',
    )

    class Meta:
        ordering = ('id',)
        permissions = (
            ('view_personal_info', 'Can view user\'s personal information'),
        )


class Post(models.Model):
    author = models.ForeignKey('User', on_delete=models.SET_NULL, related_name='posts', null=True, blank=True)
    title = models.CharField(max_length=200, blank=False)
    body = models.TextField(blank=False)
    is_published = models.BooleanField(default=False)
    show_on_main_page = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('id',)


class TaskTag(models.Model):
    name = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return "Tag object ({}:{})".format(self.id, self.name)


class Task(models.Model):
    author = models.ForeignKey('User', on_delete=models.SET_NULL, related_name='authored_tasks', null=True, blank=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(blank=True, null=False)

    flag = models.CharField(max_length=100, null=False, blank=False)

    solved_by = models.ManyToManyField('User', related_name='solved_tasks', blank=True)

    cost = models.IntegerField(null=False, blank=False, default=50)

    is_published = models.BooleanField(default=False)
    publication_time = models.DateTimeField(null=True, blank=True)

    tags = models.ManyToManyField('TaskTag', related_name='tasks', blank=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.is_published and self.publication_time is None:
            self.publication_time = timezone.now()
        elif not self.is_published and self.publication_time is not None:
            self.publication_time = None

        super(Task, self).save(force_insert=force_insert, force_update=force_update, using=using,
                               update_fields=update_fields)

    def __str__(self):
        return "Task object ({}:{})".format(self.id, self.name)

    class Meta:
        ordering = ('id',)


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

    celery_start_task_id = models.CharField(max_length=50, null=True, blank=True)
    celery_end_task_id = models.CharField(max_length=50, null=True, blank=True)

    tasks = models.ManyToManyField(
        'Task',
        related_name='contests',
        through='ContestTaskRelationship',
        blank=True
    )

    participants = models.ManyToManyField(
        'User',
        related_name='contest_participated',
        through='ContestParticipantRelationship',
        blank=True
    )

    def save(self, *args, **kwargs):
        add_start_task = False
        add_end_task = False

        if self.id:
            old = Contest.objects.only(
                'celery_start_task_id',
                'celery_end_task_id',
                'start_time',
                'end_time'
            ).get(id=self.id)

            if old.start_time != self.start_time:
                current_app.control.revoke(old.celery_start_task_id)
                if self.start_time is not None:
                    add_start_task = True

            if old.end_time != self.end_time:
                current_app.control.revoke(old.celery_end_task_id)
                if self.end_time is not None:
                    add_end_task = True

        else:
            if self.start_time is not None:
                add_start_task = True

            if self.end_time is not None:
                add_end_task = True

        super(Contest, self).save(*args, **kwargs)

        if add_start_task:
            result = celery_tasks.start_contest.apply_async(args=(self.id,), eta=self.start_time)
            self.celery_start_task_id = result.id
        if add_end_task:
            result = celery_tasks.end_contest.apply_async(args=(self.id,), eta=self.end_time)
            self.celery_end_task_id = result.id

        super(Contest, self).save()


class ContestTaskRelationship(models.Model):
    contest = models.ForeignKey('Contest', on_delete=models.CASCADE, related_name='contest_task_relationship')
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='contest_task_relationship')

    cost = models.IntegerField(default=0)
    ordering_number = models.IntegerField(default=0)

    class Meta:
        ordering = ('-ordering_number', 'cost', 'id')


class ContestParticipantRelationship(models.Model):
    contest = models.ForeignKey('Contest', on_delete=models.CASCADE, related_name='contest_participant_relationship')
    participant = models.ForeignKey('User', on_delete=models.CASCADE, related_name='contest_participant_relationship')

    last_solve = models.DateTimeField(default=timezone.now)
    delta = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = (
            'contest',
            'participant',
        )


class ContestTaskParticipantSolvedRelationship(models.Model):
    contest = models.ForeignKey(
        'Contest',
        on_delete=models.CASCADE,
        related_name='contest_task_participant_solved_relationship'
    )

    participant = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='contest_task_participant_solved_relationship'
    )

    task = models.ForeignKey(
        'Task',
        on_delete=models.CASCADE,
        related_name='contest_task_participant_solved_relationship'
    )

    class Meta:
        unique_together = (
            'contest',
            'participant',
            'task',
        )
