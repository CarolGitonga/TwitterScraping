# profiles/utils/twitter_scraper.py
import os, random
from scrapingbee import ScrapingBeeClient
from bs4 import BeautifulSoup
from django.utils import timezone
from textblob import TextBlob
from profiles.models import Profile, RawPost

NITTER_MIRRORS = [
    "https://nitter.net",
    "https://nitter.poast.org",
    "https://nitter.privacydev.net",
    "https://nitter.lucabased.xyz"
]

def scrape_twitter_profile(username: str):
    """
    Scrape Twitter profile (ScrapingBee -> Nitter fallback)
    and save tweets with sentiment analysis.
    """
    api_key = os.getenv("SCRAPINGBEE_API_KEY")
    client = ScrapingBeeClient(api_key=api_key)

    twitter_url = f"https://mobile.twitter.com/{username}"
    params = {
        "render_js": "true",
        "stealth_proxy": "true",
        "premium_proxy": "true",
        "country_code": "de",
        "wait_browser": "10000",
    }

    print(f"🕵️ Trying ScrapingBee for {username} ...")
    resp = client.get(twitter_url, params=params)
    html = None

    # --- Try ScrapingBee (Twitter) ---
    if resp.status_code == 200 and b"data-testid" in resp.content:
        html = resp.content.decode("utf-8", errors="ignore")

    # --- Fallback to Nitter ---
    if not html:
        print("⚠️ Twitter blocked the request, switching to Nitter...")
        for mirror in NITTER_MIRRORS:
            try:
                nitter_url = f"{mirror}/{username}"
                r = client.get(nitter_url)
                if r.status_code == 200:
                    html = r.content.decode("utf-8", errors="ignore")
                    print(f"✅ Using Nitter mirror: {mirror}")
                    break
            except Exception:
                continue

    if not html:
        return {"error": "All Nitter mirrors failed"}

    # --- Parse tweets ---
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.string if soup.title else username
    tweets = [div.get_text(" ", strip=True) for div in soup.select("div.tweet-content")]

    # --- Create or get Profile ---
    profile, created = Profile.objects.get_or_create(
        username=username,
        platform="Twitter",
        defaults={"full_name": title, "bio": "", "followers": 0, "following": 0},
    )

    saved_count = 0
    for text in tweets[:20]:
        if not RawPost.objects.filter(profile=profile, content=text).exists():
            # 🧠 Sentiment analysis using TextBlob
            blob = TextBlob(text)
            polarity = round(blob.sentiment.polarity, 3)  # -1.0 = negative, +1.0 = positive

            RawPost.objects.create(
                profile=profile,
                content=text,
                timestamp=timezone.now(),
                sentiment_score=polarity,
            )
            saved_count += 1

    return {
        "source": "nitter" if "nitter" in html else "twitter",
        "username": username,
        "title": title,
        "tweets_saved": saved_count,
        "total_tweets_scraped": len(tweets),
    }
