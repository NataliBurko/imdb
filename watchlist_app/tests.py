from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from .api import serializers
from . import models


#first create tests for streamplatform according to the relationships between models 
class StreamPlatformTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username="test", password="test123")
        
        login_resp = self.client.post(reverse('login'), {
            "username": "test",
            "password": "test123"
        })  

        token = login_resp.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ token)

        #create a streamplatform manually for testing
        self.stream = models.StreamPlatform.objects.create(
            name="Netflix",
            about="Streaming platform",
            website="https://netflix.com"
        )
        
        
    #try to add streamplatform being not an admin
    def test_streamplatform_create(self):
        data = {
            "name": "Netflix",
            "about": "Streaming platform",
            "website": "https://netflix.com"
        }
        
        response = self.client.post(reverse('streamplatform-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    #test to get a list of steramplatforms
    def test_streamplatform_list(self):
        response = self.client.get(reverse('streamplatform-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamplatform_detail(self):
        response = self.client.get(reverse('streamplatform-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamplatform_edit(self):
        response = self.client.put(reverse('streamplatform-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_streamplatform_delete(self):
        response = self.client.delete(reverse('streamplatform-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



class WatchListTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username="test", password="test123")
        
        login_resp = self.client.post(reverse('login'), {
            "username": "test",
            "password": "test123"
        })  

        token = login_resp.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ token) 
        
        self.stream = models.StreamPlatform.objects.create(
            name="Netflix",
            about="Streaming platform",
            website="https://netflix.com"
        ) 
        self.watchlist = models.WatchList.objects.create(platform=self.stream, title="Example Movie",
                                                        storyline="Story about Example movie", active=True )             

    def test_watchlist_create(self):
        data = {
            "platform": self.stream,
            "title": "Example Movie",
            "storyline": "Story about Example movie",
            "active": True
        }
        
        response = self.client.post(reverse('movie-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_watchlist_list(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watchlist_detail(self):
        response = self.client.get(reverse('movie-detail', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.WatchList.objects.count(), 1)
        self.assertEqual(models.WatchList.objects.get().title, 'Example Movie')

    def test_watchlist_edit(self):
        response = self.client.put(reverse('movie-detail', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_watchlist_del(self):
        response = self.client.delete(reverse('movie-detail', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ReviewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="Test", password="Test123")
        data = {
            "username": "Test",
            "password": "Test123"
        }
        log_response = self.client.post(reverse('login'), data)
        token = log_response.data['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token '+ token)

        self.streamplatform = models.StreamPlatform.objects.create(
            name="Netflix",
            about="Streaming platform",
            website="https://netflix.com"           
        ) 

        self.watchlist = models.WatchList.objects.create(
            title="Test Movie",
            storyline="About the Movie",
            platform=self.streamplatform,
            active=True
        )

        self.watchlist2 = models.WatchList.objects.create(
            title="Another Movie",
            storyline="About the Another Movie",
            platform=self.streamplatform,
            active=True
        )        

        self.review = models.Review.objects.create(
            review_user=self.user,
            rating=5,
            description="Review for watchlist2",
            watchlist=self.watchlist2,
            active=True
        )

    def test_review_create(self):
        data = {
            "review_user": self.user,            
            "rating": 5,
            "description": "Test Review",
            "watchlist": self.watchlist,
            "active": True
        }

        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Review.objects.get(id=2).description, 'Test Review')

        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_create_unauth(self):
        data = {
            "review_user": self.user,            
            "rating": 5,
            "description": "Test Review",
            "watchlist": self.watchlist,
            "active": True
        }

        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_update(self):

        review_updated = {
            "review_user": self.user,            
            "rating": 3,
            "description": "Test Review - Updated",
            "watchlist": self.watchlist,
            "active": False
        } 

        response = self.client.put(reverse('review-detail', args=(self.review.id,)), review_updated)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Review.objects.get().rating, 3)


    def test_reviews_list(self):
        response = self.client.get(reverse('review-list', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reviews_detail(self):
        response = self.client.get(reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK) 

    def test_reviews_del(self):
        response = self.client.delete(reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT) 

    def test_review_user(self):
        response = self.client.get('/watch/reviews/?username' + self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    



