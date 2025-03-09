from django.db import models
from datetime import datetime
from django.contrib.postgres.fields import ArrayField
from django.conf import settings


class TodoStatus(models.IntegerChoices):
    CREATED = 1
    WORKING = 2
    COMPLETED = 3


class Label(models.Model):
    label = models.CharField(max_length=20)


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


class BanWords(models.IntegerChoices):
    CAT = 1
    DOG = 2


class Log(models.Model):
    words = ArrayField(models.IntegerField(
        choices=BanWords.choices), null=False)
    todo = models.ForeignKey(
        Todo, on_delete=models.CASCADE, related_name='logs', null=False)

# Left Join
# Todo.objects.select_related('user_id').all()
# # Inner join
# Todo.objects.select_related('user_id').filter(user_id__isnull=False)
# # Right join from todo to user
# User.objects.select_related('todos').filter()
# # Full join complex

# # Many to many
# Todo.objects.prefetch_related('labels').all()
