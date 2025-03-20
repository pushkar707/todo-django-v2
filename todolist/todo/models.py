from django.db import models
from datetime import datetime
from django.conf import settings
from django.db.models import CheckConstraint, Q
from rest_framework.exceptions import ValidationError
from core.BaseModel import BaseModel


class TodoStatus(models.IntegerChoices):
    CREATED = 1
    WORKING = 2
    COMPLETED = 3


class Label(models.Model):
    label = models.CharField(max_length=20)


class BanWords(models.Model):
    word = models.CharField(null=False, blank=False)


class Todo(BaseModel):
    heading = models.TextField(null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    status = models.IntegerField(
        choices=TodoStatus.choices, default=TodoStatus.CREATED)
    priority = models.IntegerField(null=True, blank=True)
    created_on = models.DateTimeField(default=datetime.now)
    started_on = models.DateTimeField(null=True, blank=True)
    completed_on = models.DateTimeField(null=True, blank=True)
    due_on = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE, related_name='todos')
    is_recurring = models.BooleanField(default=False)
    labels = models.ManyToManyField(Label)
    logs = models.ManyToManyField(BanWords, related_name='todos')

    def clean(self):
        '''
        Validate status in both create and update
        Status validation created -> working -> completed
        Also checks started_on < completed_on
        '''
        if not self.pk and self.status != TodoStatus.CREATED:
            raise ValidationError(
                'Status must be created when creating the todo')
        if self.pk and self.status:
            original = Todo.objects.get(pk=self.pk)
            original_status = original.status

            if self.status == original_status:
                pass
            elif original_status == 1 and self.status != 2:
                raise ValidationError(
                    'You can only modify status from created to working')
            elif original_status == 2 and self.status != 3:
                raise ValidationError(
                    'You can only modify status from working to completed')
            elif original_status == 3:
                raise ValidationError("You cannot modify completed status")

        if self.completed_on and self.started_on and self.completed_on < self.started_on:
            raise ValidationError(
                'Completed date connot be less than starting date')
        
        if self.is_recurring and self.due_on:
            self.due_on = None

        super().clean()

    class Meta:
        # DB level constraints for started_on and completed_on
        constraints = [
            CheckConstraint(
                check=Q(completed_on__gt=models.F('started_on')),
                name='completed_on_gt_started_on'
            )
        ]
