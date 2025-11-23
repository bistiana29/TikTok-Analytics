import requests
import pandas as pd

def scrape_videos(token, hashtag, limit=50):
    """
    Scrape TikTok metadata via Apify synchronous run.
    Returns a DataFrame.
    """
    URL = f"https://api.apify.com/v2/acts/clockworks~tiktok-scraper/run-sync-get-dataset-items?token={token}"

    hashtags = []
    payload = {
        "hashtags": [hashtag],
        #"maxItems": limit,
        "resultsPerPage": limit,
        "shouldDownloadVideos": False,
        "shouldDownloadCovers": False,
        "shouldDownloadComments": False
    }

    res = requests.post(URL, json=payload)
    res.raise_for_status()

    data = res.json()
    df = pd.json_normalize(data)

    return df