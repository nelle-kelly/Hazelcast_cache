from django.core.cache.backends.base import BaseCache
from .utils import get_hazelcast_client
import hazelcast
from core.settings import HAZELCAST_CONFIG


client = get_hazelcast_client()
person_map = client.get_map("person_cache").blocking()

class HazelCastCache(BaseCache):
        
   
    def add(self, key, value, timeout=None):
        return person_map.put_if_absent(key, value) is None
    def get(self, key, default=None):
        return person_map.get(key) or default

    def set(self, key, value, timeout=None):
        person_map.put(key, value)

    def delete(self, key):
        person_map.remove(key)