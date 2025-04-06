# chemin : dpe/serializers.py

from rest_framework import serializers
from .models import *

class GaliDpeAnalyseSerializer(serializers.ModelSerializer):
    class Meta:
        model = GaliDpeAnalyse
        fields = '__all__'

class GaliDpeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GaliDpeInfo
        fields = '__all__'

        