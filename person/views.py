from django.shortcuts import render
from django.core.cache import cache
from django.http import JsonResponse
from person.models import Person

def queryset_func(data_structure_name,model_class):
    hazalcast_element = cache.get(data_structure_name)
    if not hazalcast_element:
        hazalcast_element = list(model_class.objects.values())
        cache.set(data_structure_name, hazalcast_element)
    return hazalcast_element


def get_persons(request,data_structure_name, model_class):

    #data_structure_name = model_class.lower()
    objects = queryset_func(data_structure_name, model_class)
    return JsonResponse({data_structure_name: objects})

def update_object(data_structure_name, model_class, object_id, updates):
    pass