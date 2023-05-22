from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from information.models import Event
from information.serializers import EventSerializer


class EventView(APIView):
    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EventDetailView(APIView):
    def get(self, request, event_id):
        events = get_object_or_404(Event, id=event_id)
        serializer = EventSerializer(events)
        return Response(serializer.data, status=status.HTTP_200_OK)