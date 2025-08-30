import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from typing import List
import io
from PyPDF2 import PdfReader

for resource in ['punkt', 'punkt_tab', 'stopwords']:
    try:
        nltk.data.find(f'tokenizers/{resource}')
    except LookupError:
        nltk.download(resource)

STOPWORDS_PT = set(stopwords.words('portuguese')) if 'portuguese' in stopwords.fileids() else set()
LEMMATIZER = WordNetLemmatizer()

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r'\S+@\S+', ' ', text)
    text = re.sub(r'http\S+|www.\S+', ' ', text)
    text = text.replace('\n', ' ').replace('\r', ' ')
    text = re.sub(r'\s+', ' ', text).strip()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

def tokenize_and_lemmatize(text: str) -> List[str]:
    tokens = nltk.word_tokenize(text, language='portuguese')
    tokens = [t for t in tokens if t not in STOPWORDS_PT and t.isalpha()]
    lemmas = [LEMMATIZER.lemmatize(t) for t in tokens]
    return lemmas

def preprocess_text(text: str) -> str:
    cleaned = clean_text(text)
    lemmas = tokenize_and_lemmatize(cleaned)
    return ' '.join(lemmas)

def extract_text_from_pdf_bytes(file_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(file_bytes))
    text_pages = []
    for page in reader.pages:
        text_pages.append(page.extract_text() or "")
    return "\n".join(text_pages)