from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from brewery.models import Brewery
from brewery.serializers import BrewerySerializer


class BreweryView(APIView):
    def get(self, request):
        breweries = Brewery.objects.all()
        serializer = BrewerySerializer(breweries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BreweryDetailView(APIView):
    def get(self, request, brewery_id):
        breweries = get_object_or_404(Brewery, id=brewery_id)
        serializer = BrewerySerializer(breweries)
        return Response(serializer.data, status=status.HTTP_200_OK)