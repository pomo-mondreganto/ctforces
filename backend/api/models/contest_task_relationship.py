from django.db import models

from api.models.auxiliary import CTRCurrentCostManager


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

    objects = models.Manager()
    dynamic_current_cost_annotated = CTRCurrentCostManager(dynamic=True)
    static_current_cost_annotated = CTRCurrentCostManager(dynamic=False)

    class Meta:
        unique_together = (
            'contest',
            'task',
        )

        default_manager_name = 'objects'
