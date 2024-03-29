# Generated by Django 3.0.3 on 2020-02-10 11:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0005_auto_20200210_1353'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contestparticipantrelationship',
            name='team',
        ),
        migrations.AddField(
            model_name='contestparticipantrelationship',
            name='registered_users',
            field=models.ManyToManyField(blank=True, related_name='contest_participant_relationship',
                                         to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='contestparticipantrelationship',
            name='participant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    related_name='contest_participant_relationship', to='api.Team'),
        ),
        migrations.CreateModel(
            name='CPRHelper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cpr_helpers',
                                              to='api.Contest')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cpr_helpers',
                                           to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('contest', 'user')},
            },
        ),
    ]
