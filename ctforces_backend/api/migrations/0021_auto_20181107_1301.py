# Generated by Django 2.1.2 on 2018-11-07 13:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0020_auto_20181107_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contestparticipantrelationship',
            name='contest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    related_name='contest_participant_relationship', to='api.Contest'),
        ),
        migrations.AlterField(
            model_name='contestparticipantrelationship',
            name='participant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    related_name='contest_participant_relationship', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='contesttaskrelationship',
            name='contest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    related_name='contest_task_relationship', to='api.Contest'),
        ),
        migrations.AlterField(
            model_name='contesttaskrelationship',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    related_name='contest_task_relationship', to='api.Task'),
        ),
    ]
