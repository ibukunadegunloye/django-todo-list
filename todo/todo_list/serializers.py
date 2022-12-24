from rest_framework import serializers
from .models import List

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = '__all__'