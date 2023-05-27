from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework import permissions
from review.models import Alcohol_Review, Brewery_Review, Event_Review
from review.serializers import (Alcohol_ReviewSerializer,
                                Brewery_ReviewSerializer,
                                Event_ReviewSerializer)

# Create your views here.
class Alcohol_ReviewView(APIView):
    def get(self, request):
        alc_reviews = Alcohol_Review.objects.all()
        serializer = Alcohol_ReviewSerializer(alc_reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # print(request.user)
        serializer = Alcohol_ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class Brewery_ReviewView(APIView):
    def get(self, request):
        bre_reviews = Brewery_Review.objects.all()
        serializer = Brewery_ReviewSerializer(bre_reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        # print(request.user)
        serializer = Brewery_ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Event_ReviewView(APIView):
    def get(self, request):
        eve_reviews = Event_Review.objects.all()
        serializer = Event_ReviewSerializer(eve_reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        # print(request.user)
        serializer = Event_ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Alcohol_ReviewDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, review_id):
        Alc_review = get_object_or_404(Alcohol_Review, id=review_id)
        if request.user == Alc_review.user:
        # 리뷰 삭제
            Alc_review.delete()
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