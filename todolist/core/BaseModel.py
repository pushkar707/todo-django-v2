from django.db.models import Model
from todolist.redis import redis_client
import json


class BaseModel(Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        model_name = self.__class__.__name__
        redis_client.publish(f'db_changes:{model_name}', json.dumps({
            'id': self.id,
            'operation': 'create' if is_new else 'update',
        }
        ))
