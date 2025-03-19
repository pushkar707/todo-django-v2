from todo.models import Todo
from todolist.redis import redis_client
import json


class TodoStore():

    @classmethod
    def add_todo(cls, id, heading, description, status):
        redis_client.hset('todos', id, json.dumps({
            'heading': heading, 'description': description, 'status': status
        }))

    @classmethod
    def getTodoById(cls, id):
        todo = json.loads(redis_client.hget('todos', id))
        if not todo:
            try:
                db_todo = Todo.objects.get(id=id)
                if db_todo:
                    cls.add_todo(db_todo.id, db_todo.heading,
                                 db_todo.description, db_todo.status)
                    return cls.getTodoById(db_todo.id)
            except Todo.DoesNotExist():
                return None
        return todo
