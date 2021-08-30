from collections import defaultdict

import random
from django.db import models
from django.utils import timezone


class ContestParticipantRelationship(models.Model):
    contest = models.ForeignKey(
        'api.Contest',
        on_delete=models.CASCADE,
        related_name='contest_participant_relationship',
    )
    participant = models.ForeignKey(
        'api.Team',
        on_delete=models.CASCADE,
        related_name='contest_participant_relationship',
    )

    last_solve = models.DateTimeField(default=timezone.now)
    delta = models.IntegerField(null=True, blank=True)
    opened_contest_at = models.DateTimeField(null=True, blank=True)

    randomized_tasks = models.BooleanField(default=False)

    registered_users = models.ManyToManyField(
        'User',
        related_name='contest_participant_relationship',
        blank=True,
    )

    def randomize_tasks(self):
        ctrs = list(self.contest.contest_task_relationship.all())
        random.shuffle(ctrs)
        grouped = defaultdict(list)
        for ctr in ctrs:
            grouped[ctr.main_tag_id].append(ctr)

        total = len(ctrs)
        need = self.contest.randomize_tasks_count
        left = need
        results = []
        for tag, values_iter in grouped.items():
            values = list(values_iter)
            share = round(need * len(values) / total)
            share = min(share, left)
            left -= share
            if share > len(values):
                results.extend(values)
            else:
                chosen = random.sample(values, share)
                results.extend(chosen)
        return results

    class Meta:
        unique_together = (
            'contest',
            'participant',
        )
