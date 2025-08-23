from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
#from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets

from watchlist_app.api.permissions import AdminOrReadOnly, ReviewUserOrReadOnly
from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.api.serializers import (WatchListSerializer, StreamPlatformSerializer, 
                                           ReviewSerializer)



class ReviewCreate(generics.CreateAPIView):
     serializer_class = ReviewSerializer

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

class ReviewList(generics.ListAPIView):
    # it is need to be overwritten because by default we get all reviews instead of reviews which belong to certain movie
    #queryset = Review.objects.all() 
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)

        


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]


# class ReviewDetail(mixins.RetrieveModelMixin,
#                    generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer  

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
    


# class ReviewList(mixins.ListModelMixin,
#                  mixins.CreateModelMixin,
#                  generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer




# class StreamPlatformVS(viewsets.ViewSet):

#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)
    
#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)
    
#     def create(self, request):
#         serializer = StreamPlatformSerializer(data= request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)  


# class StreamPlatformAV(APIView):

#     def get(self, request):
#         streams = StreamPlatform.objects.all()
#         serilizer = StreamPlatformSerializer(streams, many=True)
#         return Response(serilizer.data)
    
#     def post(self, request):
#         serilizer = StreamPlatformSerializer(data = request.data)
#         if serilizer.is_valid():
#             serilizer.save()
#             return Response(serilizer.data)
        
#         return Response(serilizer.errors)
    
# class StreamPltformDetailAV(APIView):

#     def get(self, request, pk):
#         try:
#             stream  = StreamPlatform.objects.get(pk=pk)
#         except StreamPlatform.DoesNotExist:
#             return Response('Not Found', status=status.HTTP_404_NOT_FOUND)
        
#         serializer = StreamPlatformSerializer(stream)
#         return Response(serializer.data)
    
#     def put(self, request, pk):
#         stream = StreamPlatform.objects.get(pk=pk)
#         serializer = StreamPlatformSerializer(stream, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
        
#         return Response(serializer.errors)
    
#     def delete(self, request, pk):
#         stream = StreamPlatform.objects.get(pk=pk)
#         stream.delete()

#         return Response('Content not found', status=status.HTTP_204_NO_CONTENT)




class WatchListAV(APIView):

    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)
        

    def post(self, request):
        serializer = WatchListSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    
class WatchListDetailAV(APIView):

    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response('Sorry, we could not find this film', status= status.HTTP_404_NOT_FOUND)
        
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)
    
    def put(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie, data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response('Content not found', status = status.HTTP_204_NO_CONTENT)



# @api_view(['GET', 'POST'])
# def movie_list(request):

#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)
        
#     if request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
            

# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_detail(request, pk):

#     if request.method == 'GET':
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response('Sorry, we could not find this film', status= status.HTTP_404_NOT_FOUND)
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
    
#     if request.method == 'PUT':
#         movie = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
    
#     if request.method == 'DELETE':
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response('Content not found', status = status.HTTP_204_NO_CONTENT)
