# profiles/views.py
from django.shortcuts import render, get_object_or_404
from django.db.models import Avg, Count
from profiles.models import Profile, RawPost

def twitter_sentiment_view(request, username):
    profile = get_object_or_404(Profile, username=username, platform="Twitter")

    # Categorize by sentiment score
    posts = RawPost.objects.filter(profile=profile)
    total = posts.count()
    positive = posts.filter(sentiment_score__gt=0.1).count()
    neutral = posts.filter(sentiment_score__range=(-0.1, 0.1)).count()
    negative = posts.filter(sentiment_score__lt=-0.1).count()

    avg_score = round(posts.aggregate(avg=Avg("sentiment_score"))["avg"] or 0, 3)

    data = {
        "profile": profile,
        "total": total,
        "positive": positive,
        "neutral": neutral,
        "negative": negative,
        "avg_score": avg_score,
    }

    return render(request, "profiles/twitter_sentiment.html", data)
