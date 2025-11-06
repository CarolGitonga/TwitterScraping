from django.urls import path
from .views import twitter_sentiment_view

urlpatterns = [
    path("twitter/sentiment/<str:username>/", twitter_sentiment_view, name="twitter_sentiment"),
]
