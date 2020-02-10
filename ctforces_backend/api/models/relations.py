from django.db import models
from django.utils import timezone

from api.models.auxiliary import CTRCurrentCostManager


class ContestTaskRelationship(models.Model):
    contest = models.ForeignKey('Contest', on_delete=models.CASCADE, related_name='contest_task_relationship')
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='contest_task_relationship')
    main_tag = models.ForeignKey(
        'TaskTag',
        on_delete=models.SET_NULL,
        related_name='contest_task_relationship_main',
        null=True,
        blank=False,
    )

    cost = models.IntegerField(default=0)
    min_cost = models.IntegerField(default=0)
    max_cost = models.IntegerField(default=0)
    decay_value = models.IntegerField(default=1)

    ordering_number = models.IntegerField(default=0)

    solved_by = models.ManyToManyField(
        'Team',
        related_name='solved_contest_tasks',
        blank=True,
    )

    objects = models.Manager()
    dynamic_current_cost_annotated = CTRCurrentCostManager(dynamic=True)
    static_current_cost_annotated = CTRCurrentCostManager(dynamic=False)

    class Meta:
        ordering = (
            '-ordering_number',
            'cost',
            'id',
        )

        unique_together = (
            'contest',
            'task',
        )

        default_manager_name = 'objects'


class ContestParticipantRelationship(models.Model):
    contest = models.ForeignKey('Contest', on_delete=models.CASCADE, related_name='contest_participant_relationship')
    participant = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='contest_participant_relationship')

    last_solve = models.DateTimeField(default=timezone.now)
    delta = models.IntegerField(null=True, blank=True)
    has_opened_contest = models.BooleanField(default=False)

    registered_users = models.ManyToManyField(
        'User',
        related_name='contest_participant_relationship',
        blank=True,
    )

    class Meta:
        unique_together = (
            'contest',
            'participant',
        )


class CPRHelper(models.Model):
    contest = models.ForeignKey('Contest', on_delete=models.CASCADE, related_name='cpr_helpers')
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='cpr_helpers')
    cpr = models.ForeignKey(
        'ContestParticipantRelationship',
        on_delete=models.CASCADE,
        related_name='cpr_helpers',
        null=True,
    )

    class Meta:
        unique_together = (
            'contest',
            'user',
        )
