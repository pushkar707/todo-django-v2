from celery import shared_task
from todo.models import Todo


@shared_task
def create_todos():
    todos = Todo.objects.prefetch_related('labels').filter(is_recurring=True)
    for todo in todos:
        new_todo = Todo.objects.create(
            heading=todo.heading, description=todo.description, priority=todo.priority, user=todo.user)
        new_todo.labels.add(*todo.labels.values_list('id', flat=True))
