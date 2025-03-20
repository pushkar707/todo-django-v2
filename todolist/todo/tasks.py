from celery import shared_task
from todo.models import Todo


@shared_task
def create_todos():
    todos = Todo.objects.prefetch_related('labels').filter(is_recurring=True)
    todo_objects = [
        Todo(heading=todo.heading, description=todo.description,
             priority=todo.priority, user=todo.user, auto_created=True)
        for todo in todos
    ]
    Todo.objects.bulk_create(todo_objects)

    for todo_object, todo in zip(todo_objects, todos):
        todo_object.labels.add(*todo.labels.values_list('id', flat=True))
