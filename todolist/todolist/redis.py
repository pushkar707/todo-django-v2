import redis
import os
from dotenv import load_dotenv
load_dotenv()

redis_client = redis.Redis(
    host=os.environ.get('REDIS_HOST'),
    port=os.environ.get('REDIS_PORT'),
    username=os.environ.get('REDIS_USERNAME'),
    password=os.environ.get('REDIS_PASSWORD')
)
pubsub = redis_client.pubsub()
