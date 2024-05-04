from django.urls import path
from . import views

urlpatterns = [
    path('ibge/', views.IBGE_get_research, name='IBGEGetResearch'),
    path('ibge/<str:ibge_id>/', views.IBGE_get_aggregated, name='IBGEGetAggregated'),
    path('ibge/<str:ibge_id>/<int:aggregate_id>/', views.IBGE_get_metadata, name='IBGEGetMetadata'),
]


