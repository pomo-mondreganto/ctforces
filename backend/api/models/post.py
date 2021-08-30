from django.db import models


class Post(models.Model):
    author = models.ForeignKey(
        'api.User',
        on_delete=models.SET_NULL,
        related_name='posts',
        null=True, blank=True,
    )

    title = models.CharField(max_length=200, blank=False)
    body = models.TextField(blank=False)

    is_published = models.BooleanField(default=False)
    show_on_main_page = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = (
            '-created_at',
            '-id',
        )
