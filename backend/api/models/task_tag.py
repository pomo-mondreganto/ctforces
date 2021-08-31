from django.core.validators import RegexValidator
from django.db import models
from django.utils.deconstruct import deconstructible


@deconstructible
class TagNameValidator(RegexValidator):
    regex = '^[a-z0-9]+(-[a-z0-9]+)*[a-z0-9]+$'
    message = 'Name must consist of words (lowercase letters and digits), divided my single dash'


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
