from django.db import models


class Submission(models.Model):
    user = models.ForeignKey(
        'api.User',
        related_name='submissions',
        null=False, blank=False,
        on_delete=models.CASCADE,
    )

    participant = models.ForeignKey(
        'api.Team',
        related_name='submissions',
        null=True, blank=True,
        on_delete=models.CASCADE,
    )

    contest = models.ForeignKey(
        'api.Contest',
        related_name='submissions',
        null=True, blank=True,
        on_delete=models.SET_NULL,
    )

    task = models.ForeignKey(
        'api.Task',
        related_name='submissions',
        null=False, blank=False,
        on_delete=models.CASCADE,
    )

    success = models.BooleanField(null=False, blank=False)
    flag = models.CharField(max_length=100, null=False, blank=False)  # same as api.Task's flag field
