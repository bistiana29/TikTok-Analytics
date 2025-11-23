import re
import pandas as pd
import emoji

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

STOPWORDS = set(stopwords.words("indonesian"))

# stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

def extract_hashtags(text):
    return re.findall(r"#\w+", text)

def extract_emoji(text):
    return [c for c in text if c in emoji.EMOJI_DATA]

# inisialisasi stemmer dan lemmatizer
porter = PorterStemmer()
lemmatizer = WordNetLemmatizer()
factory = StemmerFactory()
sastrawi_stemmer = factory.create_stemmer()

# custom stopwords (bisa ditambah sesuai kebutuhan)
CUSTOM_STOPWORDS_ID = set(['yg','dgn','dr','ke','di','tdk','nih'])
CUSTOM_STOPWORDS_EN = set(['u','ur','im','ive','lol'])  # contoh tambahan bahasa Inggris

def clean_caption(text, language='id'):
    if pd.isna(text):
        return ""
    
    # lowercase
    text = text.lower()
    
    # hilangkan hashtag
    text = re.sub(r"#\w+", " ", text)
    
    # hilangkan emoji
    text = emoji.replace_emoji(text, replace=' ')
    
    # hilangkan URL
    text = re.sub(r"http\S+|www.\S+", " ", text)
    
    # hilangkan angka & punctuation
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    
    # hilangkan extra space
    text = re.sub(r"\s+", " ", text).strip()
    
    # pilih stopwords sesuai bahasa
    if language.lower() == 'id':
        STOPWORDS_LIB = set(stopwords.words('indonesian'))
        STOPWORDS = STOPWORDS_LIB.union(CUSTOM_STOPWORDS_ID)
    else:
        STOPWORDS_LIB = set(stopwords.words('english'))
        STOPWORDS = STOPWORDS_LIB.union(CUSTOM_STOPWORDS_EN)
    
    # tokenization & remove stopwords
    tokens = [w for w in text.split() if w not in STOPWORDS]
    
    # stemming + lemmatization
    if language.lower() == 'id':
        tokens = [sastrawi_stemmer.stem(w) for w in tokens]
        # untuk bahasa Indonesia, lemmatization bisa di-skip karena stemming sudah cukup
    else:
        tokens = [porter.stem(w) for w in tokens]
        tokens = [lemmatizer.lemmatize(w) for w in tokens]
    
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