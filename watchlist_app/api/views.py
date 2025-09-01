from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.exceptions import ValidationError, Throttled
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets
from .throttling import  ReviewListThrottle

from watchlist_app.api.permissions import IsAdminOrReadOnly, IsReviewUserOrAdminOrReadOnly
from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.api.serializers import (WatchListSerializer, StreamPlatformSerializer, 
                                           ReviewSerializer)



class ReviewCreate(generics.CreateAPIView):
     serializer_class = ReviewSerializer
     permission_classes = [IsAuthenticated]
     throttle_classes = [ScopedRateThrottle]
     throttle_scope = 'review-create'


     def get_queryset(self):
         return Review.objects.all()

     def perform_create(self, serializer):
         pk = self.kwargs['pk']
         movie = WatchList.objects.get(pk=pk)
        
         review_user = self.request.user
         review_queryset = Review.objects.filter(watchlist=movie, review_user=review_user)

         if review_queryset.exists():
             raise ValidationError('You have already reviewed this movie!')
         
         if movie.number_rating == 0:
             movie.avg_rating = serializer.validated_data['rating']
         else:
             movie.avg_rating = (movie.avg_rating + serializer.validated_data['rating'])/2
        
         movie.number_rating += 1
         movie.save()

         serializer.save(watchlist=movie, review_user=review_user)


     def throttled(self, request, wait):
         msg = 'You can add only 1 comment per day.'

         raise Throttled(detail=msg)

class ReviewList(generics.ListAPIView):
    # get_queryset needs to be overwritten because by default we get all reviews instead of reviews which belong to certain movie
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewListThrottle]
    

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)
    
    def throttled(self, request, wait):
        msg = 'Too many request, see you tomorrow :)'

        raise Throttled(detail=msg)
       

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrAdminOrReadOnly]


class StreamPlatformVS(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer


class WatchListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)
        

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def throttled(self, request, wait):
        if not request.user.is_authenticated:
            msg = 'Create a free account to continue.'
        else:
            msg = 'You sent too many requests, please continue tomorrow.'
        raise Throttled(detail=msg) 
        
    
class WatchListDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [UserRateThrottle]

    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response('Sorry, we could not find this film', status= status.HTTP_404_NOT_FOUND)
        
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)
    
    def put(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response('Content not found', status = status.HTTP_204_NO_CONTENT)



