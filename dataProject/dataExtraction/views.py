import os
import requests
import tomllib
from pathlib import Path
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from .models import IBGEResearch, IBGEChildAttached
from .serializers import IBGEChildAttachedSerializer


def IBGE_get_research(request):
    def get_research(research):
        research_parent_db = list(IBGEResearch.objects.values_list('ibge_id', flat=True))
        if research['id'] not in research_parent_db:
            research_parent = IBGEResearch.objects.create(
            ibge_id=research['id'],
            research_name=research['nome'])
        
        else:
            research_parent = IBGEResearch.objects.get(ibge_id=research['id'])
        
        child_db = list(IBGEChildAttached.objects.values_list('aggregate_id', flat=True))
        child = [IBGEChildAttached(
                    parent=research_parent,
                    aggregate_id=aggregated['id'], 
                    aggregate_name=aggregated['nome'])
                for aggregated in research['agregados'] if int(aggregated['id']) not in child_db]
            
        if child:
            IBGEChildAttached.objects.bulk_create(child)
        
        return research_parent.__dict__
    
    url = 'https://servicodados.ibge.gov.br/api/v3/agregados'
    researchs_json = requests.get(url=url).json()
    
    researchs = list(map(get_research, researchs_json))
    
    context = {
        "researchs": researchs
        }
    
    return render(request, 'research.html', context)

def IBGE_get_aggregated(request, ibge_id):
    if request.is_ajax():
        research_parent = IBGEResearch.objects.get(ibge_id=ibge_id)
        children_list = IBGEChildAttached.objects.filter(parent=research_parent)
        data = [IBGEChildAttachedSerializer(child).data for child in children_list]
        
        response = {
            'aggregated_data': data
        }
        
        return JsonResponse(response)

    else:
        return HttpResponse("Error: This page can only be accessed via AJAX request.")

def IBGE_get_metadata(request, ibge_id, aggregate_id):
    if request.is_ajax():
        try:
            aggregated = IBGEChildAttached.objects.get(aggregate_id=aggregate_id)
        except ObjectDoesNotExist:
            return HttpResponse("Aggregate or entry doesn't exist.")
        
        try:
            territorial_metadata = tomllib.loads(Path(os.path.dirname(os.path.abspath(__file__))+'/metadata.toml').read_text(encoding='utf 8'))
        except TypeError as err:
            return HttpResponse(f"Territorial Level Metadata error {err}")
        except tomllib.TOMLDecodeError as err:
            return HttpResponse(f"Territorial Level Metadata wasn't decoded {err}")
        
        if not aggregated.url:
            url = f'https://servicodados.ibge.gov.br/api/v3/agregados/{aggregate_id}/metadados'
            metadata_json = requests.get(url=url).json()

            aggregated.url = metadata_json['URL']
            aggregated.research = metadata_json['pesquisa']
            aggregated.subject = metadata_json['assunto']
            aggregated.frequency = metadata_json['periodicidade']['frequencia'].capitalize()
            aggregated.start_freq = metadata_json['periodicidade']['inicio']
            aggregated.end_freq = metadata_json['periodicidade']['fim']
            
            ##### 
        return render(request, '', {})

    else:
        return HttpResponse("Error: This page can only be accessed via AJAX request.")
    