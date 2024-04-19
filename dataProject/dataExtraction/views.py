import requests
from django.http import HttpResponse
from django.shortcuts import render
from .models import IBGEResearch, IBGEChildAttached
from .serializers import IBGEResearchSerializer, IBGEChildAttachedSerializer


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
    ibge = requests.get(url=url).json()
    
    researchs = list(map(get_research, ibge))
    
    return render(request, 'research.html', {"researchs": researchs})

def IBGE_get_aggregated(request, ibge_id):
    if request.is_ajax():
        research_parent = IBGEResearch.objects.get(ibge_id=ibge_id)
        children_list = IBGEChildAttached.objects.filter(parent=research_parent)
        aggregated_children = [IBGEChildAttachedSerializer(child).data for child in children_list]
        
        data = list()
        for children in aggregated_children:
            children.aggr_reduce_label = f"{children['aggregate_name'][:100]}..."
            data.append(children)
        
        return render(request, 'research_partials/aggregated.html', {'aggregated_data': data})

    else:
        return HttpResponse("Error: This page can only be accessed via AJAX request.")
