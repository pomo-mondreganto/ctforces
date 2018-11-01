# Generated by Django 2.1.2 on 2018-11-01 15:22

import django.contrib.auth.models
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0007_auto_20181101_1039'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('upsolving_annotated', django.db.models.manager.Manager()),
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='last_solve',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]