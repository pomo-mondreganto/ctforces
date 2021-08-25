from django.db import models
from django.db.models import Count, OuterRef, Exists
from django.utils import timezone


class TaskQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)

    def with_solved_count(self):
        return self.annotate(
            solved_count=Count(
                'solved_by',
                distinct=True,
            ),
        )

    def with_solved_by_user(self, user):
        return self.annotate(
            is_solved_by_user=Exists(
                self.filter(
                    id=OuterRef('id'),
                    solved_by=user.id or -1,
                ),
            ),
        )


class Task(models.Model):
    author = models.ForeignKey(
        'api.User',
        on_delete=models.SET_NULL,
        related_name='authored_tasks',
        null=True, blank=True,
    )

    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(blank=True, null=False)

    flag = models.CharField(max_length=100, null=False, blank=False)

    solved_by = models.ManyToManyField(
        'User',
        related_name='solved_tasks',
        blank=True,
    )

    cost = models.IntegerField(null=False, blank=False, default=50)

    is_published = models.BooleanField(default=False)

    show_on_main_page = models.BooleanField(default=False)
    publication_time = models.DateTimeField(null=True, blank=True)

    tags = models.ManyToManyField(
        'api.TaskTag',
        related_name='tasks',
        blank=True,
    )

    objects = TaskQuerySet.as_manager()

    def save(self, *args, **kwargs):
        if self.is_published and self.publication_time is None:
            self.publication_time = timezone.now()
        elif not self.is_published and self.publication_time is not None:
            self.publication_time = None

        super(Task, self).save(*args, **kwargs)

    def __str__(self):
        return f"Task {self.name} ({self.id})"

    class Meta:
        ordering = ('id',)
