# profiles/utils/wordcloud_gen.py
import io, base64
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from profiles.models import RawPost

def generate_wordcloud_base64(username, platform="Twitter"):
    """
    Dynamically generate a WordCloud and return it as a base64-encoded string.
    """
    posts = RawPost.objects.filter(profile__username=username, profile__platform=platform)
    text = " ".join([p.content for p in posts if p.content])

    if not text.strip():
        return None

    wc = WordCloud(
        width=1000,
        height=600,
        background_color="white",
        colormap="viridis",
        max_words=200
    ).generate(text)

    # Convert to image bytes in memory
    buffer = io.BytesIO()
    plt.figure(figsize=(10, 6))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(buffer, format="png")
    plt.close()
    buffer.seek(0)

    # Encode to base64 for embedding
    image_base64 = base64.b64encode(buffer.read()).decode("utf-8")
    buffer.close()
    return image_base64
