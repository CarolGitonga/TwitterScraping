from django.urls import path
from .views import twitter_entity_graph_view, twitter_heatmap_view, twitter_sentiment_view, twitter_timeline_view, twitter_wordcloud_view

urlpatterns = [
    path("twitter/sentiment/<str:username>/", twitter_sentiment_view, name="twitter_sentiment"),
    path("twitter/wordcloud/<str:username>/", twitter_wordcloud_view, name="twitter_wordcloud"),
    path("twitter/timeline/<str:username>/", twitter_timeline_view, name="twitter_timeline"),
    path("twitter/heatmap/<str:username>/", twitter_heatmap_view, name="twitter_heatmap"),
     path("twitter/entities/<str:username>/", twitter_entity_graph_view, name="twitter_entities"),
]
