from django.db import models
from django.db.models import (
    Count,
    F,
    Value as V,
    Exists,
    OuterRef,
    BooleanField,
)
from django.db.models.functions import Coalesce, Ceil, Greatest


class ContestTaskRelationshipQuerySet(models.QuerySet):
    def with_dynamic_cost(self):
        return self.with_solved_count().annotate(
            current_cost=Greatest(
                Ceil(
                    (F('min_cost') - F('max_cost')) /
                    (F('decay_value') * F('decay_value')) *
                    (F('solved_count') * F('solved_count')) +
                    F('max_cost')
                ),
                F('min_cost'),
            ),
        )

    def with_static_cost(self):
        return self.with_solved_count().annotate(current_cost=F('cost'))

    def with_solved_by_team(self, team):
        if not team:
            sq = V(0, output_field=BooleanField())
        else:
            sq = Exists(
                team.contest_task_relationship_solved.filter(
                    id=OuterRef('id'),
                ),
            )
        return self.annotate(is_solved_by_user=sq)

    def with_solved_on_upsolving(self, user):
        if not user.is_authenticated:
            sq = V(0, output_field=BooleanField())
        else:
            sq = Exists(
                user.solved_tasks.filter(
                    id=OuterRef('task_id'),
                ),
            )
        return self.annotate(is_solved_on_upsolving=sq)

    def with_solved_count(self):
        return self.annotate(
            solved_count=Coalesce(
                Count(
                    'solved_by',
                    distinct=True,
                ),
                V(0),
            ),
        )


class ContestTaskRelationship(models.Model):
    contest = models.ForeignKey(
        'api.Contest',
        on_delete=models.CASCADE,
        related_name='contest_task_relationship',
    )
    task = models.ForeignKey(
        'api.Task',
        on_delete=models.CASCADE,
        related_name='contest_task_relationship',
    )
    main_tag = models.ForeignKey(
        'api.TaskTag',
        on_delete=models.SET_NULL,
        null=True, blank=False,
    )

    cost = models.IntegerField(default=0)
    min_cost = models.IntegerField(default=0)
    max_cost = models.IntegerField(default=0)
    decay_value = models.IntegerField(default=1)

    solved_by = models.ManyToManyField(
        'Team',
        related_name='contest_task_relationship_solved',
        blank=True,
    )

    objects = ContestTaskRelationshipQuerySet.as_manager()

    class Meta:
        unique_together = (
            'contest',
            'task',
        )
