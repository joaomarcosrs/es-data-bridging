import requests
from django.http import HttpResponse
from django.shortcuts import render


def testGetIbGE(request):
    url = 'https://servicodados.ibge.gov.br/api/v3/agregados'
    ibge = requests.get(url=url)
    
    return HttpResponse(ibge)

