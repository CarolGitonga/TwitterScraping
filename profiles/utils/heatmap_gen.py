# profiles/utils/heatmap_gen.py
import io
import base64
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from profiles.models import RawPost

def generate_activity_heatmap(username, platform="Twitter"):
    """
    Generate an activity heatmap (day vs hour) for a user's posts.
    Returns a base64-encoded PNG string.
    """
    posts = RawPost.objects.filter(profile__username=username, profile__platform=platform)
    timestamps = [p.timestamp for p in posts if p.timestamp]

    if not timestamps:
        return None

    df = pd.DataFrame({"timestamp": timestamps})
    df["day"] = df["timestamp"].dt.day_name()
    df["hour"] = df["timestamp"].dt.hour

    # Reorder days for better readability
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    df["day"] = pd.Categorical(df["day"], categories=day_order, ordered=True)

    # Pivot table: count of posts per (day, hour)
    pivot = df.pivot_table(index="day", columns="hour", aggfunc="size", fill_value=0)

    # Plot the heatmap
    plt.figure(figsize=(12, 6))
    sns.heatmap(pivot, cmap="YlGnBu", linewidths=0.3, annot=False)
    plt.title(f"Posting Activity Heatmap for @{username}")
    plt.xlabel("Hour of Day")
    plt.ylabel("Day of Week")

    # Convert plot to base64
    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format="png")
    plt.close()
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode("utf-8")
    buffer.close()

    return image_base64
