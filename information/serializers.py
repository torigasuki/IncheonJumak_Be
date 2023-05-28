from rest_framework import serializers
from information.models import Event


class EventSerializer(serializers.ModelSerializer):
    alchol_name = serializers.SerializerMethodField()

    def get_alchol_name(self, obj):
        return obj.alchol.name
    
    class Meta:
        model = Event
        fields = '__all__'