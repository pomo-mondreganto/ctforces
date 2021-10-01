import secrets

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from guardian.shortcuts import assign_perm


class Team(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False, unique=True)
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


@receiver(post_save, sender=Team)
def on_team_saved(instance, **_kwargs):
    assign_perm('view_team', instance.captain, instance)
    assign_perm('change_team', instance.captain, instance)
    assign_perm('delete_team', instance.captain, instance)
    assign_perm('register_team', instance.captain, instance)
