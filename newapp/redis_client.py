import redis
from django.conf import settings
import ssl  # Add this

redis_client = redis.Redis.from_url(
    settings.UPSTASH_REDIS_URL,
    decode_responses=True,
    socket_timeout=10,
    retry_on_timeout=True,
    ssl_cert_reqs=None,  # Add this for SSL bypass if needed
)