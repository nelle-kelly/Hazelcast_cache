# hazelcast_cache/helpers.py

from django.core.cache.backends.base import BaseCache
from .utils import get_hazelcast_client
import hazelcast
#from core.settings import HAZELCAST_CONFIG


client = get_hazelcast_client()
#person_map = client.get_map("person_cache").blocking()


"""les testes se trouvent dans le fichier person_test avec l'utilisation de HazelcastCache"""
class HazelCastCache(BaseCache):
    def __init__(self, location, params):
        
        super().__init__(params)
        self.structures = {}  # Cache local pour les différentes structures Hazelcast

    def _get_structure(self, structure_name, structure_type):
        
        if structure_name not in self.structures:
            if structure_type == "map":
                self.structures[structure_name] = client.get_map(structure_name).blocking()
            elif structure_type == "set":
                self.structures[structure_name] = client.get_set(structure_name).blocking()
            elif structure_type == "queue":
                self.structures[structure_name] = client.get_queue(structure_name).blocking()
            else:
                raise ValueError(f"Type de structure Hazelcast inconnu : {structure_type}")
        return self.structures[structure_name]

    def add(self, structure_name, structure_type, key, value=None, timeout=None):
       
        structure = self._get_structure(structure_name, structure_type)
        if structure_type == "map":
            return structure.put_if_absent(key, value) is None
        elif structure_type == "set":
            return structure.add(key)  # Les sets ajoutent directement l'élément
        else:
            raise ValueError(f"Opération non supportée pour le type : {structure_type}")

    def get(self, structure_name, structure_type, key, default=None):
       
        structure = self._get_structure(structure_name, structure_type)
        if structure_type == "map":
            return structure.get(key) or default
        elif structure_type == "set":
            return key in structure  # Vérifie si l'élément est présent dans le set
        else:
            raise ValueError(f"Opération non supportée pour le type : {structure_type}")

    def set(self, structure_name, structure_type, key, value=None, timeout=None):
       
        structure = self._get_structure(structure_name, structure_type)
        if structure_type == "map":
            structure.put(key, value)
        elif structure_type == "set":
            structure.add(key)
        else:
            raise ValueError(f"Opération non supportée pour le type : {structure_type}")

    def delete(self, structure_name, structure_type, key):
       
        structure = self._get_structure(structure_name, structure_type)
        if structure_type == "map":
            structure.remove(key)
        elif structure_type == "set":
            structure.remove(key)
        else:
            raise ValueError(f"Opération non supportée pour le type : {structure_type}")