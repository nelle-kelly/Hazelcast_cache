# person/tests.py
from django.test import TestCase
from person.models import Person
from hazelcast_cache.utils import get_hazelcast_client
import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hazelcast_demo.core.settings")
django.setup()

client = get_hazelcast_client()
person_map = client.get_map("person_cache").blocking()

class HazelcastCacheTestCase(TestCase):

     def add_person(self):

        people_data = [
        {"first_name": "Ahmed", "last_name": "Ali", "phone": "123456789", "email": "ahmed@example.com"},
        {"first_name": "Chaimae", "last_name": "Ben", "phone": "987654321", "email": "chaimae@example.com"},
        {"first_name": "Jalila", "last_name": "Doe", "phone": "555666777", "email": "jalila@example.com"},
        {"first_name": "Othmane", "last_name": "Smith", "phone": "444333222", "email": "othmane@example.com"},
        {"first_name": "Fatima", "last_name": "Zahra", "phone": "111222333", "email": "fatima@example.com"},
         ]

       
        for person_data in people_data:
            person, created = Person.objects.get_or_create(**person_data)
            if created:
                print(f"Ajouté: {person.first_name} {person.last_name}")
            else:
                print(f"Déjà existant: {person.first_name} {person.last_name}")