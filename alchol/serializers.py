from rest_framework import serializers
from alchol.models import Alchol


class AlcholSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alchol
        fields = "__all__"

class AlcholListSerializer(serializers.ModelSerializer):
    # user = serializers.SerializerMethodField()

    # def get_user(self, obj):
    #     return obj.user.username

    class Meta:
        model = Alchol
        fields = "__all__"