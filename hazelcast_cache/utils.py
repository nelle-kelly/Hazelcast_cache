from hazelcast import HazelcastClient
from core.settings import HAZELCAST_CONFIG

def get_hazelcast_client():
   config = HAZELCAST_CONFIG
   client = HazelcastClient(**config)
   return client