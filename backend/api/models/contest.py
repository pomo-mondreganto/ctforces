from celery import current_app
from django.db import models
from django.db.models import (
    IntegerField,
    BooleanField,
    DateTimeField,
    OuterRef,
    Value as V,
    Count,
    Subquery,
    Exists,
)
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.utils.functional import cached_property

from api import celery_tasks
from api.database_functions import SubquerySum
from .contest_participant_relationship import ContestParticipantRelationship
from .contest_task_relationship import ContestTaskRelationship
from .cpr_helper import CPRHelper


class ContestQuerySet(models.QuerySet):
    def with_participant_count(self):
        return self.annotate(
            registered_count=Count('participants', distinct=True),
        )

    def with_user_registered(self, user):
        if user.is_authenticated:
            annotation = Exists(
                CPRHelper.objects.filter(
                    user=user,
                    contest=OuterRef('id'),
                ),
            )
        else:
            annotation = V(0, output_field=BooleanField())
        return self.annotate(is_registered=annotation)

    def only_published(self):
        return self.filter(is_published=True)

    def only_upcoming(self, at=None):
        if at is None:
            at = timezone.now()
        return self.filter(start_time__gt=at)

    def only_running(self, at=None):
        if at is None:
            at = timezone.now()
        return self.filter(start_time__lte=at, end_time__gt=at)

    def only_finished(self, at=None):
        if at is None:
            at = timezone.now()
        return self.filter(end_time__lte=at)

    def with_opened_at(self, user):
        if user.is_authenticated:
            annotation = Subquery(
                ContestParticipantRelationship.objects.filter(
                    contest=OuterRef('id'),
                    participant__participants=user,
                ).values('opened_contest_at')[:1],
            )
        else:
            annotation = V(None, output_field=DateTimeField)

        return self.annotate(opened_at=annotation)


class Contest(models.Model):
    author = models.ForeignKey(
        'api.User',
        on_delete=models.SET_NULL,
        related_name='contests_authored',
        null=True, blank=True
    )

    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField()

    start_time = models.DateTimeField(null=False, blank=False)
    end_time = models.DateTimeField(null=False, blank=False)

    is_published = models.BooleanField(default=False)
    is_registration_open = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    public_scoreboard = models.BooleanField(default=True)

    publish_tasks_after_finished = models.BooleanField(default=True)
    is_rated = models.BooleanField(default=True)
    always_recalculate_rating = models.BooleanField(default=False)
    dynamic_scoring = models.BooleanField(default=False)

    is_virtual = models.BooleanField(default=False)
    virtual_duration = models.DurationField(
        help_text='Virtual participation duration ([DD] [HH:[MM:]]ss[.uuuuuu])',
        null=True, blank=True,
    )

    celery_end_task_id = models.CharField(max_length=50, null=True, blank=True)
    processed_end_task = models.BooleanField(default=False)

    tasks = models.ManyToManyField(
        'api.Task',
        related_name='contests',
        through='api.ContestTaskRelationship',
        blank=True,
    )

    participants = models.ManyToManyField(
        'api.Team',
        related_name='contests_participated',
        through='api.ContestParticipantRelationship',
        blank=True,
    )

    objects = ContestQuerySet.as_manager()

    def reset_end_action(self):
        if self.celery_end_task_id:
            current_app.control.revoke(self.celery_end_task_id)
        result = celery_tasks.on_contest_ended.apply_async(args=(self.id,), eta=self.end_time)
        self.celery_end_task_id = result.id

    def save(self, *args, **kwargs):
        if not self.id or Contest.objects.only('end_time').get(id=self.id).end_time != self.end_time:
            self.reset_end_action()

        super(Contest, self).save(*args, **kwargs)

    @cached_property
    def is_upcoming(self, at=None):
        if at is None:
            at = timezone.now()
        return at < self.start_time

    @cached_property
    def is_running(self, at=None):
        if at is None:
            at = timezone.now()
        return self.start_time <= at < self.end_time

    @cached_property
    def is_finished(self, at=None):
        if at is None:
            at = timezone.now()
        return self.end_time <= at

    def get_cpr(self, user, prefetch=False):
        qs = CPRHelper.objects.filter(
            contest=self,
            user=user.id,
        )
        if prefetch:
            qs = qs.select_related('cpr__participant')
        return getattr(qs.first(), 'cpr', None)

    def get_participating_team(self, user):
        cpr = self.get_cpr(user, prefetch=True)
        return getattr(cpr, 'participant', None)

    def is_virtually_running_for(self, user, at=None):
        if not self.is_virtual:
            return False
        if at is None:
            at = timezone.now()
        if at < self.start_time:
            return False

        cpr = self.get_cpr(user)
        if not cpr:
            return False
        opened_at = cpr.opened_contest_at
        if not opened_at:
            return False
        end = min(self.end_time, opened_at + self.virtual_duration)
        return at < end

    def __str__(self):
        return f"Contest object ({self.id}:{self.name})"

    def get_scoreboard_relations_queryset(self):
        task_relations = ContestTaskRelationship.objects.all()
        if self.dynamic_scoring:
            task_relations = task_relations.with_dynamic_cost()
        else:
            task_relations = task_relations.with_static_cost()

        participant_cost_sum_subquery = SubquerySum(
            task_relations.filter(
                contest=self,
                solved_by=OuterRef('participant_id'),
            ).values('current_cost'),
            output_field=IntegerField(),
            field_name='current_cost',
        )

        relations = self.contest_participant_relationship.select_related(
            'participant',
        ).annotate(
            cost_sum=Coalesce(participant_cost_sum_subquery, V(0)),
        ).order_by('-cost_sum', 'last_solve')

        return relations
