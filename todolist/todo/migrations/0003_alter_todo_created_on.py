# Generated by Django 5.1.7 on 2025-03-20 10:07

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_todo_auto_created_alter_todo_completed_on_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='created_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
