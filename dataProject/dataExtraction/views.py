import requests
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from .models import IBGEResearch, IBGEChildAttached


def IBGE_get_research(request):
    def get_research(research):
        try:
            research_parent = IBGEResearch.objects.get(ibge_id=research['id'])
        
        except:
            research_parent = IBGEResearch.objects.create(
                ibge_id=research['id'],
                research_name=research['nome'])
        
        aggregated_child = list()
        for aggregated in research['agregados']:
            try:
                child = IBGEChildAttached.objects.get(aggregate_id=aggregated['id'])
            
            except:
                child = IBGEChildAttached(
                    parent=research_parent,
                    aggregate_id=aggregated['id'], 
                    aggregate_name=aggregated['nome'])
                aggregated_child.append(child)
        
        if aggregated_child:
            IBGEChildAttached.objects.bulk_create(aggregated_child)
        
        return research_parent.__dict__
    
    url = 'https://servicodados.ibge.gov.br/api/v3/agregados'
    ibge = requests.get(url=url).json()
    
    researchs = list(map(get_research, ibge))
    
    return render(request, 'dashboard.html', {"researchs": researchs})


