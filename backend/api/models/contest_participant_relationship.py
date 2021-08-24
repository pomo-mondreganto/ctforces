from django.db import models
from django.utils import timezone


class ContestParticipantRelationship(models.Model):
    contest = models.ForeignKey(
        'api.Contest',
        on_delete=models.CASCADE,
        related_name='contest_participant_relationship',
    )
    participant = models.ForeignKey(
        'api.Team',
        on_delete=models.CASCADE,
        related_name='contest_participant_relationship',
    )

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
