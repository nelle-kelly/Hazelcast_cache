from hazelcast import HazelcastClient
from core.settings import HAZELCAST_CONFIG

def get_hazelcast_client():
   client = HazelcastClient(**HAZELCAST_CONFIG)
   return client