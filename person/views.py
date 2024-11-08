from django.shortcuts import render
from django.core.cache import cache
from django.http import JsonResponse
from person.models import Person

def get_persons(request):
    persons = cache.get("persons")
    if not persons:
        persons = list(Person.objects.values())
        cache.set("persons", persons)
    return JsonResponse({"persons": persons})
