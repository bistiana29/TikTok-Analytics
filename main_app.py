import os
import re
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from wordcloud import WordCloud
from streamlit_option_menu import option_menu

from src.scraping.video_scraping import scrape_videos
from src.cleaning.video_cleaning import clean_video_df
from src.anlysis.engagement import authors_videos, likes_analysis, comment_analysis, share_analysis, saved_analysis, views_analysis, duration_analysis, videos_over_time, likes_over_time
from src.anlysis.keyword_hashtag import hashtags_association

# Setup halaman utama
st.set_page_config(
    page_title="I'm Ticky🤗",
    page_icon="🎵",
    layout="wide"
)

# Styling CSS
st.markdown("""
<style>

    /* Background utama */
    [data-testid="stAppViewContainer"] {
        background-color: #FFFFFF;
    }

    /* Sidebar background */
    section[data-testid="stSidebar"] {
        background-color: #F87B1B !important;
    }

    /* Semua teks dalam sidebar jadi putih */
    section[data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }

    /* Judul Sidebar */
    .sidebar-title {
        font-size: 18px;
        font-weight: bold;
        color: #FFFFFF;
        text-align: center;
        margin-top: -10px;
        margin-bottom: 10px;
    }

    /* Option Menu - container */
    div[data-testid="stSidebar"] .nav-link {
        border-radius: 8px;
        margin: 3px 0px !important;
    }

    /* Normal state */
    div[data-testid="stSidebar"] .nav-link:not(.active) {
        background-color: #F87B1B !important; 
        color: #FFFFFF !important;
    }

    /* Hover state */
    div[data-testid="stSidebar"] .nav-link:hover {
        background-color: #D96D17 !important;
        color: #FFFFFF !important;
    }

    /* Selected */
    div[data-testid="stSidebar"] .nav-link.active {
        background-color: #11224E !important;
        color: #FFFFFF !important;
    }

    /* "Card" styling untuk konten */
    .metric-card {
        background-color: #EEEEEE;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }

</style>
""", unsafe_allow_html=True)

if "selected_page" not in st.session_state:
    st.session_state["selected_page"] = "Home"

with st.sidebar:
    st.markdown('<div class="sidebar-title">TikTok Analytics and Keyword Insight</div>', unsafe_allow_html=True)

    selected = option_menu(
        menu_title=None,
        options=["Home", "Engagement", "Keyword and Hashtag"],
        icons=["house", "bar-chart", "chat-dots"],
        default_index=["Home", "Engagement", "Keyword and Hashtag"].index(st.session_state["selected_page"]),
        orientation="vertical",
        styles={
            "container": {"background-color": "#F87B1B", "padding": "0px"},
            "icon": {"color": "white", "font-size": "20px"},
            "nav-link": {
                "color": "white",
                "font-size": "14px",
                "padding": "7px",
                "margin": "5px 0px",
            },
            "nav-link-selected": {
                "background-color": "#11224E",
                "color": "white",
            }
        }
    )

    # Footer
    st.markdown(
        "<p style='color:white; margin-top:200px;'>© miggy2025</p>",
        unsafe_allow_html=True
    )
st.session_state["selected_page"] = selected

if selected == "Home":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    IMG_PATH = os.path.join(BASE_DIR, "assets", "home_image.png")

    # Gambar berdampingan dengan teks
    col1, col2 = st.columns([3, 5])

    with col1:
        st.markdown("""
            <h1 style="font-size:40px; margin-bottom:0;">
                Hi! Ticky here 🤗
            </h1>
            <p style="font-size:20px; color:#555;">
                Ready to analyze your TikTok keywords. Enter your Apify token and keyword or hashtag to get started!
            </p>
        """, unsafe_allow_html=True)

    with col2:
        st.image(IMG_PATH, use_column_width=True)

    # User input di HALAMAN, bukan sidebar
    token = st.text_input("🔑 Apify Token", type="password")
    if token:
        st.session_state['api_token'] = token

    hashtag = st.text_input("🏷️ Hashtag or Keyword", placeholder="e.g., mbg, skincare, ruu")
    limit = st.slider("📦 Number of Videos", 10, 700, 50)

    start_btn = st.button("🚀 Start")

    if start_btn:
        if not token or not hashtag:
            st.warning("Please enter both token and hashtag first.")
            st.stop()

        with st.spinner("Scraping TikTok data..."):
            df_raw = scrape_videos(token, hashtag, limit)
            df = clean_video_df(df_raw)

        st.session_state["video_df"] = df
        st.success(f"Scraping selesai! Total video: {len(df)}")

        # Directly navigate to Page 2
        st.session_state["selected_page"] = "Engagement"
        st.rerun()

elif selected == "Engagement":
    if "video_df" not in st.session_state:
        st.error("⚠ No data available. Please scrape data first on the Home page.")
        st.stop()

    df = st.session_state["video_df"]
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    IMG_PATH = os.path.join(BASE_DIR, "assets", "engagement_image.png")

    # Gambar berdampingan dengan teks
    col1, col2 = st.columns([5, 2])

    with col1:
        st.markdown("""
            <h1 style="font-size:40px; margin-bottom:0;">
                Engagement Analysis Dashboard
            </h1>
        """, unsafe_allow_html=True)

    with col2:
        st.image(IMG_PATH, use_column_width=True)

    col3, col4, col5 = st.columns(3)
    with col3:
        # Card total videos
        total_videos = len(df)
        st.markdown(f"""
        <style>
        .metric-card {{
            background-color: #11224E;  /* warna card */
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
            margin-bottom: 10px;
        }}
        .metric-label {{
            font-size: 16px;
            opacity: 0.7;
        }}
        .metric-value {{
            font-size: 28px;
            font-weight: bold;
            margin-top: 5px;
        }}
        </style>
        <div class="metric-card">
            <div class="metric-label">Total Videos</div>
            <div class="metric-value">{total_videos}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        # Card total authors
        total_authors = df['authorMeta.name'].nunique()
        st.markdown(f"""
        <div class="metric-card" style="background-color: #11224E;">
            <div class="metric-label">Total Authors</div>
            <div class="metric-value">{total_authors}</div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        # Card total days covered
        total_days = (df['createTimeISO'].max() - df['createTimeISO'].min()).days + 1
        st.markdown(f"""
        <div class="metric-card" style="background-color: #11224E;">
            <div class="metric-label">Days Covered</div>
            <div class="metric-value">{total_days}</div>
        </div>
        """, unsafe_allow_html=True)

    # grafik
    st.plotly_chart(videos_over_time(df), use_container_width=True)
    st.plotly_chart(likes_over_time(df), use_container_width=True)

    st.plotly_chart(authors_videos(df), use_container_width=True)
    st.plotly_chart(likes_analysis(df), use_container_width=True)
    st.plotly_chart(comment_analysis(df), use_container_width=True)
    st.plotly_chart(share_analysis(df), use_container_width=True)
    st.plotly_chart(saved_analysis(df), use_container_width=True)
    st.plotly_chart(views_analysis(df), use_container_width=True)
    st.plotly_chart(duration_analysis(df), use_container_width=True)

    # tabel engagement rate
    required_cols = ['authorMeta.name', 'webVideoUrl', 'diggCount', 'commentCount',
        'shareCount', 'collectCount', 'playCount']

    missing_cols = [c for c in required_cols if c not in df.columns]
    if missing_cols:
        st.error(f"Kolom berikut tidak ditemukan di dataset: {missing_cols}")
    else:
        engagement_rate = df[required_cols].copy()

        # Hitung Engagement Rate
        engagement_rate['engagement_rate'] = (
            engagement_rate['diggCount']
            + engagement_rate['commentCount']
            + engagement_rate['shareCount']
            + engagement_rate['collectCount']
        ) / engagement_rate['playCount'].replace(0, np.nan) * 100

        # Bersihkan nilai inf/nan
        engagement_rate['engagement_rate'] = (engagement_rate['engagement_rate'].replace([np.inf, -np.inf], np.nan).fillna(0).round(2))
        engagement_rate = engagement_rate.sort_values(by='engagement_rate', ascending=False).reset_index(drop=True)
        engagement_rate["No"] = np.arange(1, len(engagement_rate) + 1)

        st.subheader("📊 Engagement Rate Ranking")
        engagement_rate["engagement_rate_for_bar"] = (engagement_rate["engagement_rate"].clip(0, 100))

        columns_to_show = ["No", "authorMeta.name", "webVideoUrl",
                           "diggCount", "commentCount", "shareCount",
                            "collectCount", "playCount", "engagement_rate_for_bar"]
        st.dataframe(
            engagement_rate[columns_to_show],
            column_config={
                "No": st.column_config.NumberColumn("No", format="%d"),
                
                "engagement_rate_for_bar": st.column_config.ProgressColumn(
                    "Engagement Rate (%)",
                    help="(likes + comments + shares + bookmarks) / views * 100",
                    format="%.2f",
                    min_value=0,
                    max_value=100.0,
                ),
                "engagement_rate": st.column_config.NumberColumn(
                    "Engagement Rate (raw)",
                    format="%.2f",
                    help="Nilai asli sebelum clip (bisa >100%)"
                ),
            },
            column_order=columns_to_show,  # Hanya kolom ini yang tampil
            hide_index=True,
            use_container_width=True
        )

elif selected == "Keyword and Hashtag":
    if "video_df" not in st.session_state:
        st.error("⚠ No data available. Please scrape data first on the Home page.")
        st.stop()

    df = st.session_state["video_df"]

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    IMG_PATH = os.path.join(BASE_DIR, "assets", "teks_image.png")

    col1, col2 = st.columns([5, 2])

    with col1:
        st.markdown("""
            <h1 style="font-size:40px; margin-bottom:0;">
                Keyword and Hashtag Analysis
            </h1>
        """, unsafe_allow_html=True)

    with col2:
        st.image(IMG_PATH, use_column_width=True)

    def generate_wordcloud(text, title):
        wc = WordCloud(
            width=800,
            height=400,
            background_color="white",
            colormap="viridis"
        ).generate(text)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wc, interpolation="bilinear")
        ax.set_title(title, fontsize=18)
        ax.axis("off")
        return fig

    st.subheader("💬 WordCloud Analysis")

    # Caption
    caption_text = " ".join(df["text_clean"].astype(str).tolist())
    st.write("### 📝 Caption WordCloud")
    st.pyplot(generate_wordcloud(caption_text, "Caption WordCloud"))

    # Hashtag
    def clean_hashtags(text):
        tags = re.findall(r"#\w+", str(text))
        return " ".join(tags)

    hashtag_text = " ".join(df["hashtags"].apply(clean_hashtags).tolist())
    st.write("### #️⃣ Hashtag WordCloud")
    st.pyplot(generate_wordcloud(hashtag_text, "Hashtag WordCloud"))

    # Emoji
    emoji_list = df["emoji"].dropna().astype(str).tolist()
    emoji_list = [e for e in emoji_list if e.strip() != ""]

    st.write("### 😊 Emoji Caption WordCloud")

    if len(emoji_list) == 0:
        st.info("⚠ No emoji found in captions")
    else:
        emoji_text = " ".join(emoji_list)  # gabungkan menjadi string
        try:
            st.pyplot(generate_wordcloud(emoji_text, "Emoji WordCloud"))
        except ValueError as ve:
            st.warning(f"WordCloud Emoji Failed: {ve}")

    # Analisis Asosiasi Hashtag
    st.write('### ⛓️ Hashtag Association Network')
    df_top_pairs, fig_assoc = hashtags_association(df, top_n_pairs=30)

    # tampilkan di Streamlit
    col3, col4 = st.columns([3,2])
    with col3:
        st.plotly_chart(fig_assoc)
    with col4:
        st.dataframe(df_top_pairs)