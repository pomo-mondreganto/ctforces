from django.db import models
from django.utils import timezone


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


class ContestParticipantRelationship(models.Model):
    contest = models.ForeignKey('Contest', on_delete=models.CASCADE, related_name='contest_participant_relationship')
    participant = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='contest_participant_relationship')

    last_solve = models.DateTimeField(default=timezone.now)
    delta = models.IntegerField(null=True, blank=True)
    has_opened_contest = models.BooleanField(default=False)

    class Meta:
        unique_together = (
            'contest',
            'participant',
        )
