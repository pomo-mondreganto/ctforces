from django.db import models

from api.storages import DefaultStorage
from .auxiliary import (
    CustomUploadTo,
    CustomFileField,
)


class TaskFile(models.Model):
    owner = models.ForeignKey(
        'api.User',
        on_delete=models.SET_NULL,
        related_name='files',
        null=True, blank=True,
    )
    task = models.ForeignKey(
        'api.Task',
        on_delete=models.SET_NULL,
        related_name='files',
        null=True, blank=True,
    )

    name = models.CharField(max_length=100, null=False, blank=False)

    upload_time = models.DateTimeField(auto_now_add=True)

    file_field = CustomFileField(
        upload_to=CustomUploadTo(
            upload_type='files',
            path='',
            append_random=True,
        ),
        storage=DefaultStorage(),
        blank=False, null=False,
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return f"TaskFile for {self.task_id} ({self.id})"
