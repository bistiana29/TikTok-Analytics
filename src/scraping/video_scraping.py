import requests
import pandas as pd

def scrape_videos(token, limit=100):
    url = f"https://api.apify.com/v2/acts/clockworks~tiktok-scraper/runs/last/dataset/items"
    params = {
        "token": token,
        "clean": "false",
        "limit": limit,
        "status": "SUCCEEDED"
    }
    res = requests.get(url, params=params)
    res.raise_for_status()
    data = res.json()
    df = pd.json_normalize(data)
    return df