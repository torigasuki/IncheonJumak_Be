from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework import permissions
from alchol.models import Alchol
from brewery.models import Brewery
from information.models import Event
from review.models import Alcohol_Review, Brewery_Review, Event_Review
from review.serializers import (Alcohol_ReviewSerializer, Alcohol_ReviewCreateSerializer,
                                Brewery_ReviewSerializer, Brewery_ReviewCreateSerializer,
                                Event_ReviewSerializer, Event_ReviewCreateSerializer,)

# Create your views here.
class ShowMyReview(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, user_id):
        data={}
        my_alc_reviews = Alcohol_Review.objects.filter(user=user_id).order_by('-created_at')[:5]
        my_bre_reviews = Brewery_Review.objects.filter(user=user_id).order_by('-created_at')[:5]
        my_eve_reviews = Event_Review.objects.filter(user=user_id).order_by('-created_at')[:5]
        if my_alc_reviews:
            alc_serializer = Alcohol_ReviewSerializer(my_alc_reviews, many=True)
            try:
                data['reviews'] += alc_serializer.data
            except:
                data['reviews'] = alc_serializer.data
        if my_bre_reviews:
            bre_serializer = Brewery_ReviewSerializer(my_bre_reviews, many=True)
            try:
                data['reviews'] += bre_serializer.data
            except:
                data['reviews'] = bre_serializer.data
        if my_eve_reviews:
            eve_serializer = Event_ReviewSerializer(my_eve_reviews, many=True)
            try:
                data['reviews'] += eve_serializer.data
            except:
                data['reviews'] = eve_serializer.data
        return Response(data, status=status.HTTP_200_OK)


class Alcohol_ReviewView(APIView):
    permission_classes =[permissions.IsAuthenticatedOrReadOnly]
    def get(self, request):
        alc_reviews = Alcohol_Review.objects.all().order_by('-created_at')
        serializer = Alcohol_ReviewSerializer(alc_reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, alchol_id):        
        alchol = Alchol.objects.get(id=alchol_id)
        serializer = Alcohol_ReviewCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, alchol=alchol)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, review_id):
        alc_review = get_object_or_404(Alcohol_Review, id=review_id)
        if request.user == alc_review.user:
        # 리뷰 삭제
            alc_review.delete()
            return Response("댓글이 삭제되었습니다", status=status.HTTP_204_NO_CONTENT)
        # 댓글 작성자 != 로그인한 유저
        return Response("본인이 작성한 댓글만 삭제할수 있습니다", status=status.HTTP_403_FORBIDDEN)
    

class Brewery_ReviewView(APIView):
    parser_classes =[permissions.IsAuthenticatedOrReadOnly]
    def get(self, request):
        bre_reviews = Brewery_Review.objects.all()
        serializer = Brewery_ReviewSerializer(bre_reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, brewery_id):        
        brewery = Brewery.objects.get(id=brewery_id)
        serializer = Brewery_ReviewCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, brewery=brewery)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, review_id):
        brew_review = get_object_or_404(Brewery_Review, id=review_id)
        if request.user == brew_review.user:
        # 리뷰 삭제
            brew_review.delete()
            return Response("댓글이 삭제되었습니다", status=status.HTTP_204_NO_CONTENT)
        # 댓글 작성자 != 로그인한 유저
        return Response("본인이 작성한 댓글만 삭제할수 있습니다", status=status.HTTP_403_FORBIDDEN)




class Event_ReviewView(APIView):
    [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request):
        eve_reviews = Event_Review.objects.all()
        serializer = Event_ReviewSerializer(eve_reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, event_id):        
        event = Event.objects.get(id=event_id)
        serializer = Event_ReviewCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, information=event)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, review_id):
        eve_review = get_object_or_404(Event_Review, id=review_id)
        if request.user == eve_review.user:
        # 리뷰 삭제
            eve_review.delete()
            return Response("댓글이 삭제되었습니다", status=status.HTTP_204_NO_CONTENT)
        # 댓글 작성자 != 로그인한 유저
        return Response("본인이 작성한 댓글만 삭제할수 있습니다", status=status.HTTP_403_FORBIDDEN)



# class CommentView(APIView):
#     def get(self, request):
#         pass
#     def post(self, request):
#         pass

# class CommentDetailView(APIView):
#     def put(self, request):
#         pass
#     def delete(self, request):
#         pass
    
# class LikeView(APIView):
#     def post(self, request):
#         pass