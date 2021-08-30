from django.db import models


class TaskHint(models.Model):
    author = models.ForeignKey(
        'api.User',
        on_delete=models.SET_NULL,
        related_name='hints',
        null=True, blank=True,
    )
    task = models.ForeignKey(
        'api.Task',
        on_delete=models.CASCADE,
        related_name='hints',
        null=False, blank=False,
    )

    is_published = models.BooleanField(default=False)

    body = models.TextField(null=False, blank=True)

    def __str__(self):
        return f"TaskHint for {self.task_id} ({self.id})"
