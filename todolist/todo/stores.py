from todo.models import Todo


class TodoStore():
    todos = {}

    @classmethod
    def add_todo(cls, id, heading, description, status):
        cls.todos[id] = {
            'heading': heading, 'description': description, 'status': status
        }

    @classmethod
    def getTodoById(cls, id):
        todo = cls.todos.get(id)
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
