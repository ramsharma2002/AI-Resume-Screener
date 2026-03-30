import nltk, string
from nltk.corpus import stopwords
nltk.download('stopwords')

def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    words = text.split()
    stop_words = set(stopwords.words("english"))
    return " ".join(w for w in words if w not in stop_words)
