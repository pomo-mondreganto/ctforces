from django.db import models

from .auxiliary import TagNameValidator


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
