import redis
from django.conf import settings

redis_client = redis.from_url(settings.UPSTASH_REDIS_URL)
