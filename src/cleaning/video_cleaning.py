import re
import emoji
import pandas as pd
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

STOPWORDS = set(stopwords.words("indonesian"))

# stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

def extract_hashtags(text):
    return re.findall(r"#\w+", text)

def extract_emoji(text):
    return [c for c in text if c in emoji.EMOJI_DATA]

def clean_caption(text):
    if pd.isna(text):
        return ""

    # lowercase
    text = text.lower()

    # hilangkan hashtag (akan dipisah)
    text = re.sub(r"#\w+", " ", text)

    # hilangkan emoji
    text = emoji.replace_emoji(text, replace=' ')

    # hilangkan URL
    text = re.sub(r"http\S+|www.\S+", " ", text)

    # hilangkan angka & punctuation
    text = re.sub(r"[^a-zA-Z\s]", " ", text)

    # hilangkan extra space
    text = re.sub(r"\s+", " ", text).strip()

    # remove stopwords
    tokens = [w for w in text.split() if w not in STOPWORDS]

    # stemming
    tokens = [stemmer.stem(w) for w in tokens]

    return " ".join(tokens)

def clean_video_df(df_raw):
    """Membersihkan DataFrame hasil scraping video TikTok."""

    df = df_raw.copy()
    columns_needed = [
        'authorMeta.name',
        'text',
        'diggCount',
        'shareCount',
        'playCount',
        'commentCount',
        'collectCount',
        'videoMeta.duration',
        'createTimeISO',
        'webVideoUrl'
    ]
    df = df[columns_needed]

    # drop duplikat
    df = df.drop_duplicates().reset_index(drop=True)

    df['createTimeISO'] = pd.to_datetime(df['createTimeISO'])
    df["hashtags"] = df["text"].apply(extract_hashtags)
    df["emoji"] = df["text"].apply(extract_emoji)
    df["text_clean"] = df["text"].apply(clean_caption)

    return df