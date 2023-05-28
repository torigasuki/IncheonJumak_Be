from rest_framework import serializers
from brewery.models import Brewery


class BrewerySerializer(serializers.ModelSerializer):
    alchol_name = serializers.SerializerMethodField()

    def get_alchol_name(self, obj):
        return obj.alchol.name
        
    
    class Meta:
        model = Brewery
        fields ='__all__'