from django.db import models
import json


class IBGEParentAttached(models.Model):
    ibge_id = models.CharField(max_length=2, blank=False)
    name = models.CharField(max_length=255)
    
class IBGEChildAttached(models.Model):
    parent = models.ForeignKey(IBGEParentAttached, on_delete=models.CASCADE, related_name='child_aggregated')
    aggregate_id = models.IntegerField(blank=False)
    aggregate_name = models.CharField(max_length=400)
    url = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    frequency_choices = [
        ('P1', 'Anual'),
        ('P8', 'Semestral'),
        ('P9', 'Trimestral'),
        ('P5', 'Mensal'),
        ('P13', 'Trimestral móvel')
    ]
    frequency = models.CharField(max_length=5, choices=frequency_choices)
    start_freq = models.PositiveIntegerField()
    end_freq = models.PositiveIntegerField()
    territorial_level = models.ManyToManyField('TerritorialLevel')
    
class IBGETerritorialLevel(models.Model):
    territorial_id = models.CharField(max_length=10)
    territorial_name = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.territorial_name
    
class IBGEvariables(models.Model):
    var_id = models.IntegerField()
    name = models.CharField(max_length=250)
    unity = models.CharField(max_length=50)
    summarization = models.CharField(max_length=100)
    
    def set_summarization(self, summary):
        self.summarization = json.dumps(summary)

    def get_summarization(self):
        return json.loads(self.summarization)

