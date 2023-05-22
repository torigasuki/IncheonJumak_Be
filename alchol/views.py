from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from alchol.models import Alchol
from alchol.serializers import AlcholSerializer


class AlcholView(APIView):
    def get(self, request):
        alchols = Alchol.objects.all()
        serializer = AlcholSerializer(alchols, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AlcholCategoryView(APIView):
    def get(self, request, sort):
        alchols = Alchol.objects.filter(sort=sort)
        serializer = AlcholSerializer(alchols, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AlcholDetailView(APIView):
    def get(self, request, alchol_id):
        alchol = get_object_or_404(Alchol, id=alchol_id)
        serializer = AlcholSerializer(alchol)
        return Response(serializer.data, status=status.HTTP_200_OK)