from rest_framework import serializers
from . import models


class IBGEResearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IBGEResearch
        fields = '__all__'
        
class IBGEChildAttachedSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IBGEChildAttached
        fields = '__all__'