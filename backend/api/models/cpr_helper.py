from django.db import models


class CPRHelper(models.Model):
    contest = models.ForeignKey(
        'api.Contest',
        on_delete=models.CASCADE,
        related_name='cpr_helpers',
    )
    user = models.ForeignKey(
        'api.User',
        on_delete=models.CASCADE,
        related_name='cpr_helpers',
    )
    cpr = models.ForeignKey(
        'api.ContestParticipantRelationship',
        on_delete=models.CASCADE,
        related_name='cpr_helpers',
        null=True,
    )

    class Meta:
        unique_together = (
            'contest',
            'user',
        )
