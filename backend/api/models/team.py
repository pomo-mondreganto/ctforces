import secrets

from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=25, null=False, blank=False, unique=True)
    join_token = models.CharField(max_length=255, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    rating = models.IntegerField(default=2000)
    max_rating = models.IntegerField(default=2000)

    captain = models.ForeignKey(
        'api.User',
        on_delete=models.SET_NULL,
        related_name='teams_captain',
        null=True, blank=True,
    )

    participants = models.ManyToManyField(
        'api.User',
        related_name='teams',
        blank=True,
    )

    @staticmethod
    def gen_join_token(name):
        return f'{name}:{secrets.token_hex(16)}'

    class Meta:
        ordering = ('id',)
        permissions = (
            ('register_team', 'Can register teams for a contest'),
        )
