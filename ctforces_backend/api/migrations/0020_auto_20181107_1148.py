# Generated by Django 2.1.2 on 2018-11-07 11:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0019_auto_20181104_0819'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('is_published', models.BooleanField(default=False)),
                ('is_running', models.BooleanField(default=False)),
                ('is_finished', models.BooleanField(default=False)),
                ('is_registration_open', models.BooleanField(default=False)),
                ('celery_start_task_id', models.CharField(blank=True, max_length=50, null=True)),
                ('celery_end_task_id', models.CharField(blank=True, max_length=50, null=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                             related_name='contests_authored', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ContestParticipantRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_solve', models.DateTimeField(auto_now_add=True)),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Contest')),
                ('participant',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ContestTaskRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.IntegerField(default=0)),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Contest')),
                ('solved', models.ManyToManyField(blank=True, related_name='contest_task_relationship',
                                                  to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Task')),
            ],
        ),
        migrations.AddField(
            model_name='contest',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='contest_participated',
                                         through='api.ContestParticipantRelationship', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contest',
            name='tasks',
            field=models.ManyToManyField(blank=True, related_name='contests', through='api.ContestTaskRelationship',
                                         to='api.Task'),
        ),
    ]