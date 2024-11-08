from hazelcast_cache.utils import get_hazelcast_client
from person.models import Person
import os
import django
from django.core.cache import cache

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hazelcast_demo.core.settings")
django.setup()

client = get_hazelcast_client()
person_map = client.get_map("person_cache").blocking()

def persons_data():
    people_data = [
        {"first_name": "Ahmed", "last_name": "Ali", "phone": "123456789", "email": "ahmed@example.com"},
        {"first_name": "Chaimae", "last_name": "Ben", "phone": "987654321", "email": "chaimae@example.com"},
        {"first_name": "Jalila", "last_name": "Doe", "phone": "555666777", "email": "jalila@example.com"},
        {"first_name": "Othmane", "last_name": "Smith", "phone": "444333222", "email": "othmane@example.com"},
        {"first_name": "Fatima", "last_name": "Zahra", "phone": "111222333", "email": "fatima@example.com"},
    ]
    
    for person_data in people_data:
        person = Person.objects.create(**person_data)
        print(f"Ajouté: {person.first_name} {person.last_name}")

def getData_persons():
    # Exécute le queryset et stocke les résultats en cache
    persons = Person.objects.all()
    print("Personnes récupérées de la base de données:")
    for person in persons:
        print({"id": person.id, "first_name": person.first_name, "last_name": person.last_name, 
               "phone": person.phone, "email": person.email})

    # Stocke la liste des objets dans le cache Django
    cache.set('persons', persons, timeout=60*15)  #pour 15 minutes

def getPerson_cache():

    persons = cache.get('persons')
    # Vérifie que les objets existent dans le cache avant de les manipuler
    if persons is None:
        print("Exécutez getData_persons() d'abord ")
        return
    
    print("Personnes récupérées du cache Django :")
    for person in persons:
        print({
            "id": person.id, 
            "first_name": person.first_name, 
            "last_name": person.last_name, 
            "phone": person.phone, 
            "email": person.email
        })

def put_persons_cache_Hazelcast():

    persons = cache.get('persons')

    for person in persons:
        person_map.put(person.id, {
            "first_name": person.first_name,
            "last_name": person.last_name,
            "phone": person.phone,
            "email": person.email
        })
    
    # Récupère et affiche les objets depuis le cache Hazelcast
    #cached_persons = [person_map.get(person.id) for person in persons]
    print("\nPersonnes récupérées du cache Hazelcast:")
    for person in persons:
        cached_person = cache.get(f"person_{person.id}")
        print(cached_person)  

if __name__ == "__main__":
    persons_data()
    getData_persons()
    getPerson_cache()
    put_persons_cache_Hazelcast()
