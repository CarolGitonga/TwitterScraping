from django.urls import path
from .views import twitter_sentiment_view, twitter_timeline_view, twitter_wordcloud_view

urlpatterns = [
    path("twitter/sentiment/<str:username>/", twitter_sentiment_view, name="twitter_sentiment"),
    path("twitter/wordcloud/<str:username>/", twitter_wordcloud_view, name="twitter_wordcloud"),
    path("twitter/timeline/<str:username>/", twitter_timeline_view, name="twitter_timeline"),
]
