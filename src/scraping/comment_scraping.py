# import requests
# import pandas as pd
# import math


# def _fetch_comments_from_apify(token, video_url, max_items):
#     """
#     Fetch raw comments from Apify TikTok Comments Scraper.
#     Only retrieves main comments.
#     """

#     url = f"https://api.apify.com/v2/acts/clockworks~tiktok-comments-scraper/run-sync-get-dataset-items?token={token}"

#     payload = {
#         "videoUrl": video_url,     
#         "maxComments": max_items, 
#         "depth": 1                
#     }

#     res = requests.post(url, json=payload, timeout=120)
#     res.raise_for_status()

#     data = res.json()
#     df = pd.json_normalize(data)

#     if "parentCommentId" in df.columns:
#         df = df[df["parentCommentId"].isna()].reset_index(drop=True)

#     return df

# def _sample_size(total_comments, threshold_comment, small_video_percent, big_video_percent):
#     if total_comments < threshold_comment:
#         ratio = small_video_percent
#     else:
#         ratio = big_video_percent

#     return max(1, math.ceil(total_comments * ratio))


# def scrape_comments(df_videos,
#                     token,
#                     threshold_comment=50,
#                     small_video_percent=0.20,
#                     big_video_percent=0.10):

#     all_results = []

#     for _, row in df_videos.iterrows():
#         video_url = row.get("webVideoUrl")
#         total_comments = int(row.get("commentCount", 0))

#         if not video_url or total_comments == 0:
#             continue

#         sample_n = _sample_size(total_comments, threshold_comment,
#                                 small_video_percent, big_video_percent)

#         try:
#             df_comments = _fetch_comments_from_apify(
#                 token=token,
#                 video_url=video_url,
#                 max_items=sample_n * 5
#             )

#             if df_comments.empty:
#                 continue

#             if len(df_comments) > sample_n:
#                 df_comments = df_comments.sample(n=sample_n, random_state=42)

#             df_comments["videoUrl"] = video_url
#             df_comments["videoAuthor"] = row.get("authorMeta.name", "")

#             all_results.append(df_comments)

#         except Exception as e:
#             print(f"[ERROR] Gagal scrape komentar untuk {video_url}: {e}")

#     if not all_results:
#         return pd.DataFrame()

#     return pd.concat(all_results, ignore_index=True)