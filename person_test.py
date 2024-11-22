from hazelcast_cache.utils import get_hazelcast_client
from person.models import Person
from hazelcast_cache.helpers import HazelCastCache
import os
import django
from django.core.cache import cache

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hazelcast_demo.core.settings")
django.setup()

client = get_hazelcast_client()
#person_map = client.get_map("person_cache").blocking()
hazelcast_cache = HazelCastCache(location=None, params={})
person_map = client.get_map("persons").blocking()
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
    cache.set('persons', 'map', '',persons )  #pour 15 minutes """timeout=60*15"""

def getPerson_cache():

    persons = cache.get('persons', 'map', '')
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

    persons = cache.get('persons', 'map', '')
    if not persons:
        print("Aucune personne trouvée dans le cache Django.")
        return

    for person in persons:
        hazelcast_cache.set('persons', 'map', person.id, {
            "first_name": person.first_name,
            "last_name": person.last_name,
            "phone": person.phone,
            "email": person.email
        })
    
        hazelcast_cache.set('persons', 'map',person.last_name, {
            "first_name": person.first_name,
            "last_name": person.last_name,
            "phone": person.phone,
            "email": person.email
        })
    
    print("\nPersonnes récupérées du cache Hazelcast:")
    for person in persons:
        cached_person =  hazelcast_cache.get('persons', 'map',person.id) 
        print(cached_person)  

def get_one_person(first_name):
    cached_person = hazelcast_cache.get("person", "map", first_name)
    if cached_person is not None:
        print(f"Personne trouvée dans le cache Hazelcast avec ID {first_name}:")
        print(cached_person)
    else:
        print(f"Aucune personne trouvée dans le cache Hazelcast avec ID {first_name}.")


def update_person_cache(person_id, updated_field, new_value):
    # Met à jour un champ spécifique d'une personne dans le cache Hazelcast
    cached_person = hazelcast_cache.get("persons", "map", person_id) # modifier uniquement un element  est-ce possible0
    if cached_person is not None:
        cached_person[updated_field] = new_value
        hazelcast_cache.set("persons", "map", person_id, cached_person)
        print(f"Personne mise à jour dans le cache Hazelcast : {cached_person}")
    else:
        print(f"Aucune personne trouvée dans le cache Hazelcast avec ID {person_id}.")



###reponse a la problematique de la modification d'un champ d'un objet dans Hcast######################################


""" Dans Hazelcast, les objets stockés ne peuvent pas être modifiés 
directement sur place. Chaque modification nécessite de récupérer l'objet, 
de le modifier en mémoire, puis de le remettre à jour dans le cache. C'est dû à la nature immuable des valeurs stockées dans le cache.

Mais, Hazelcast offre une solution plus optimisée via EntryProcessors, qui permettent d'appliquer des modifications directement sur le serveur Hazelcast sans transférer l'ensemble des données entre le client et le serveur. 
Cette option réduit la surcharge mémoire et le gaspillage réseau.

voici un exemple: """
def update_field_entry_processor(field, value):
    """
    Crée un script EntryProcessor pour mettre à jour un champ d'une personne.
    """
    script = f"""
        if (entry.getValue() != null) {{
            entry.getValue().put("{field}", "{value}");
            entry.setValue(entry.getValue());
        }}
    """
    return script
def update_person_cache_optimized(person_id, updated_field, new_value):
    """
    Met à jour uniquement un champ spécifique d'une personne dans le cache Hazelcast.
    """
    try:
        # Créer l'EntryProcessor pour mettre à jour le champ
        entry_processor_script = update_field_entry_processor(updated_field, new_value)
        
        
        person_map.execute_on_key(person_id, entry_processor_script)
        
        print(f"Le champ '{updated_field}' de la personne avec ID {person_id} a été mis à jour.")
    except Exception as e:
        print(f"Erreur lors de la mise à jour de la personne dans Hazelcast : {e}")





if __name__ == "__main__":
    persons_data()
    getData_persons()
    getPerson_cache()
    put_persons_cache_Hazelcast()
    get_one_person()
    
