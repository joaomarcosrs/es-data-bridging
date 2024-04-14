from django.db import models
import json


class IBGEParentAttached(models.Model):
    ibge_id = models.CharField(max_length=2, blank=False)
    name = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.name
    
    def __dict__(self):
        return {'id': self.ibge_id, 'name': self.name}
    
class IBGEChildAttached(models.Model):
    parent = models.ForeignKey(IBGEParentAttached, on_delete=models.CASCADE, related_name='child_aggregated')
    aggregate_id = models.IntegerField(blank=False)
    aggregate_name = models.CharField(max_length=500)
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
    territorial_level = models.ManyToManyField('IBGETerritorialLevel')
    variables = models.ManyToManyField('IBGEVariables')
    classifications = models.ManyToManyField('IBGEClassifications')
    
class IBGETerritorialLevel(models.Model):
    territorial_id = models.CharField(max_length=10)
    territorial_name = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.territorial_name
    
class IBGEVariables(models.Model):
    var_id = models.IntegerField()
    variable_name = models.CharField(max_length=250)
    unity = models.CharField(max_length=50)
    summarization = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.variable_name
    
    def set_summarization(self, summary):
        self.summarization = json.dumps(summary)

    def get_summarization(self):
        return json.loads(self.summarization)

class IBGEClassifications(models.Model):
    classifc_id = models.IntegerField()
    classifc_name = models.CharField(max_length=50)
    status = models.BooleanField()
    exceptions = models.CharField(max_length=100)
    category = models.ManyToManyField('IBGECategories')
    
    def __str__(self) -> str:
        return self.classifc_name
    
    def set_exceptions(self, excpt):
        self.exceptions = json.dumps(excpt)

    def get_exceptions(self):
        return json.loads(self.exceptions)
    
class IBGECategories(models.Model):
    category_id = models.IntegerField()
    category_name = models.CharField(max_length=100)
    unity = models.CharField(max_length=50)
    level = models.SmallIntegerField()
    
    def __str__(self) -> str:
        return self.category_name