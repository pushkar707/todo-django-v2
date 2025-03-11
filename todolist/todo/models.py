from django.db import models
from datetime import datetime
from django.conf import settings
from django.db.models import CheckConstraint, Q


class TodoStatus(models.IntegerChoices):
    CREATED = 1
    WORKING = 2
    COMPLETED = 3


class Label(models.Model):
    label = models.CharField(max_length=20)


class BanWords(models.Model):
    word = models.CharField(null=False, blank=False)


class Todo(models.Model):
    heading = models.TextField(null=False, blank=False)
    description = models.TextField(null=True)
    status = models.IntegerField(
        choices=TodoStatus.choices, default=TodoStatus.CREATED)
    priority = models.IntegerField(null=True)
    created_on = models.DateTimeField(default=datetime.now)
    started_on = models.DateTimeField(null=True)
    completed_on = models.DateTimeField(null=True)
    due_on = models.DateTimeField(null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE, related_name='todos')
    is_recurring = models.BooleanField(default=False)
    labels = models.ManyToManyField(Label)
    logs = models.ManyToManyField(BanWords,  null=False, related_name='todos')

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(completed_on__gt=models.F('started_on')),
                name='completed_on_gt_started_on'
            )
        ]
