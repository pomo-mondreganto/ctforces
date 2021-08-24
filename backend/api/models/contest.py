from celery import current_app
from django.db import models
from django.db.models import IntegerField, OuterRef, Value as V
from django.db.models.functions import Coalesce

from api import celery_tasks
from api.database_functions import SubquerySum
from .contest_task_relationship import ContestTaskRelationship


class Contest(models.Model):
    author = models.ForeignKey(
        'api.User',
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

    def get_scoreboard_relations_queryset(self):
        if self.dynamic_scoring:
            manager = ContestTaskRelationship.dynamic_current_cost_annotated
        else:
            manager = ContestTaskRelationship.static_current_cost_annotated

        participant_cost_sum_subquery = SubquerySum(
            manager.filter(
                contest=self,
                solved_by__id=OuterRef('participant_id'),
            ).values('current_cost'),
            output_field=IntegerField(),
            field_name='current_cost',
        )

        relations = self.contest_participant_relationship.select_related(
            'participant',
        ).annotate(
            cost_sum=Coalesce(participant_cost_sum_subquery, V(0)),
        ).order_by('-cost_sum', 'last_solve')

        if not self.always_recalculate_rating:
            relations = relations.filter(has_opened_contest=True)

        return relations
