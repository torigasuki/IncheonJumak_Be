from rest_framework import serializers
from review.models import Alcohol_Review, Brewery_Review, Event_Review

class Alcohol_ReviewSerializer(serializers.ModelSerializer):
    table = serializers.SerializerMethodField()

    def get_table(self, obj):
        table = self.Meta.model._meta.db_table
        return table.split('_')[1]

    class Meta:
        model = Alcohol_Review
        fields = ('id', 'content', 'updated_at', 'table','user')


class Brewery_ReviewSerializer(serializers.ModelSerializer):
    table = serializers.SerializerMethodField()

    def get_table(self, obj):
        table = self.Meta.model._meta.db_table
        return table.split('_')[1]

    class Meta:
        model = Brewery_Review
        fields = ('id', 'content', 'updated_at', 'table','user')


class Event_ReviewSerializer(serializers.ModelSerializer):
    table = serializers.SerializerMethodField()

    def get_table(self, obj):
        table = self.Meta.model._meta.db_table
        return table.split('_')[1]
    
    class Meta:
        model = Event_Review
        fields = ('id', 'content', 'updated_at', 'table','user')
        
        
class Alcohol_ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alcohol_Review
        fields = ["content",]

class Brewery_ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brewery_Review
        fields = ["content",]


class Event_ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event_Review
        fields = ["content",]
        
class Alcohol_ReviewListSerializer(serializers.ModelSerializer):
    # user = serializers.SerializerMethodField()
    
    # def get_user(self, obj):
    #     return obj.user.email
    
    class Meta:
        model = Alcohol_Review
        fields = ("pk", "content", "updated_at") 

class Brewery_ReviewListSerializer(serializers.ModelSerializer):
    # user = serializers.SerializerMethodField()
    
    # def get_user(self, obj):
    #     return obj.user.email
    
    class Meta:
        model = Brewery_Review
        fields = ("pk", "content", "updated_at") 

class Event_ReviewListSerializer(serializers.ModelSerializer):
    # user = serializers.SerializerMethodField()
    
    # def get_user(self, obj):
    #     return obj.user.email
    
    class Meta:
        model = Event_Review
        fields = ("pk", "content", "updated_at") 