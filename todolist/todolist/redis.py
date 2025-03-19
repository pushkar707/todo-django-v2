import redis

redis_client = redis.Redis()
pubsub = redis_client.pubsub()
