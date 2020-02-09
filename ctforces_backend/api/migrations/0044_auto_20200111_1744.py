# Generated by Django 2.2 on 2020-01-11 14:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0043_user_telegram'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='dynamic_scoring',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contesttaskparticipantsolvedrelationship',
            name='contest_task_relation',
            field=models.ForeignObject(blank=True, from_fields=('contest_id', 'task_id'), null=True,
                                       on_delete=django.db.models.deletion.CASCADE,
                                       related_name='contest_task_participant_solved_relationship',
                                       to='api.ContestTaskRelationship', to_fields=('contest_id', 'task_id')),
        ),
        migrations.AddField(
            model_name='contesttaskrelationship',
            name='max_cost',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='contesttaskrelationship',
            name='min_cost',
            field=models.IntegerField(default=0),
        ),
    ]