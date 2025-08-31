import re
import string
import spacy
from typing import List
import io
from PyPDF2 import PdfReader

nlp = spacy.load("pt_core_news_sm")

def clean_text(text: str) -> str:
    """
    Limpa o texto:
    - coloca em minúsculo
    - remove e-mails, URLs, quebras de linha
    - remove múltiplos espaços
    - remove pontuação
    """
    text = text.lower()
    text = re.sub(r'\S+@\S+', ' ', text)
    text = re.sub(r'http\S+|www.\S+', ' ', text)
    text = text.replace('\n', ' ').replace('\r', ' ')
    text = re.sub(r'\s+', ' ', text).strip()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

def tokenize_and_lemmatize(text: str) -> List[str]:
    """
    Tokeniza e lematiza usando spaCy:
    - remove stopwords
    - remove tokens que não são palavras (pontuação, números, etc.)
    """
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return tokens

def preprocess_text(text: str) -> str:
    """
    Executa o pipeline completo de pré-processamento:
    1. limpeza
    2. tokenização + lematização
    """
    cleaned = clean_text(text)
    lemmas = tokenize_and_lemmatize(cleaned)
    return " ".join(lemmas)

def extract_text_from_pdf_bytes(file_bytes: bytes) -> str:
    """
    Extrai texto de um arquivo PDF a partir de bytes.
    """
    reader = PdfReader(io.BytesIO(file_bytes))
    text_pages = []
    for page in reader.pages:
        text_pages.append(page.extract_text() or "")
    return "\n".join(text_pages)
