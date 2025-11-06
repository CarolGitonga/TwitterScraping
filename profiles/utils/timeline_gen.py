# profiles/utils/timeline_gen.py
import pandas as pd
import plotly.express as px
from django.utils import timezone
from profiles.models import RawPost

def generate_timeline_html(username, platform="Twitter"):
    """
    Generate a dynamic Plotly timeline for all posts of a user.
    Returns HTML string that can be embedded in a Django template.
    """
    posts = RawPost.objects.filter(profile__username=username, profile__platform=platform).order_by("timestamp")
    data = [
        {"timestamp": p.timestamp, "sentiment": p.sentiment_score, "content": p.content[:100]}
        for p in posts if p.timestamp
    ]
    if not data:
        return None

    df = pd.DataFrame(data)
    df["date"] = df["timestamp"].dt.date

    # Count posts per day + average sentiment
    grouped = df.groupby("date").agg(
        posts=("content", "count"),
        avg_sentiment=("sentiment", "mean")
    ).reset_index()

    # --- Create interactive Plotly figure ---
    fig = px.bar(
        grouped,
        x="date",
        y="posts",
        title=f"Posting Frequency Timeline for @{username}",
        labels={"date": "Date", "posts": "Number of Posts"},
        color="avg_sentiment",
        color_continuous_scale="RdYlGn",
    )
    fig.update_layout(template="plotly_white", xaxis_title="Date", yaxis_title="Posts")

    # Return HTML div
    return fig.to_html(full_html=False)
