# hazelcast_cache/helpers.py

from django.core.cache.backends.base import BaseCache
from .utils import get_hazelcast_client
import hazelcast

# Initialiser le client Hazelcast et la map pour le cache
client = get_hazelcast_client()
person_map = client.get_map("person_cache").blocking()

class HazelCastCache(BaseCache):
    def __init__(self, location, params):
        # Passer uniquement `params` à la classe parente BaseCache
        super().__init__(params)
        
    def add(self, key, value, timeout=None):
        return person_map.put_if_absent(key, value) is None

    def get(self, key, default=None):
        return person_map.get(key) or default

    def set(self, key, value, timeout=None):
        person_map.put(key, value)

    def delete(self, key):
        person_map.remove(key)
