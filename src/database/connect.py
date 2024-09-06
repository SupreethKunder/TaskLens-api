import redis
from ..core.config import settings
from supabase import create_client, Client

redis_client = redis.Redis.from_url(settings.REDIS_URL)
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
