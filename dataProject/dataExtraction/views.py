import requests
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from .models import IBGEParentAttached, IBGEChildAttached


def IBGE_get_research(request):
    def get_research(research):
        ibge_research = IBGEParentAttached(ibge_id=research['id'], name=research['nome'])
        
        return ibge_research.__dict__()
    
    url = 'https://servicodados.ibge.gov.br/api/v3/agregados'
    ibge = requests.get(url=url).json()
    
    list(map(get_research, ibge))
    
    context = list(map(get_research, ibge))
    
    return JsonResponse(context, safe=False)
    # return render(request, 'dashboard.html', {"context": context})


