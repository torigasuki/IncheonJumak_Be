from rest_framework import serializers
from brewery.models import Brewery


class BrewerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Brewery
        fields = "__all__"


class BreweryListSerializer(serializers.ModelSerializer):
    # user = serializers.SerializerMethodField()

    # def get_user(self, obj):
    #     return obj.user.username

    class Meta:
        model = Brewery
        fields = "__all__"