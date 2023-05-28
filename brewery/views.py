from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from brewery.models import Brewery
from brewery.serializers import BrewerySerializer
from review.serializers import Brewery_ReviewSerializer
from rest_framework.pagination import PageNumberPagination

    
class BreweryPagination(PageNumberPagination):
    page_size = 4 #임의 페이지 수 설정해놨으니 후에 수정하면 됨


class BreweryView(APIView):
    pagination_class = BreweryPagination
    serializer_class = BrewerySerializer
    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        else:
            pass
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset,self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)
    
    def get(self, request):
        breweries = Brewery.objects.all().order_by('id') # 순서 오류가 나서 일단 'id'순으로 정렬, 나중에 변경해도 됨
        page = self.paginate_queryset(breweries)
        serializer = BrewerySerializer(breweries, many=True)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(breweries, many=True)        
        return Response(serializer.data, status=status.HTTP_200_OK)


class BreweryDetailView(APIView):
    def get(self, request, brewery_id):
        breweries = get_object_or_404(Brewery, id=brewery_id)
        serializer = BrewerySerializer(breweries)
        reviews = breweries.brewery_review.all()
        brew_serializer = Brewery_ReviewSerializer(reviews, many=True)
        return Response({'brewery': serializer.data, 'reviews': brew_serializer.data}, status=status.HTTP_200_OK)