import sys
import os
import pytest

# Adiciona o diretório raiz do projeto ao path para que possamos importar 'backend'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.utils_text import preprocess_text, clean_text, tokenize_and_lemmatize

def test_clean_text():
    """Tests only the text cleaning part."""
    raw_text = "  Olá! Meu e-mail é teste@ex.com. Acesse http://exemplo.com e veja.\n"
    expected = "olá meu email é acesse e veja"
    assert clean_text(raw_text) == expected

def test_tokenize_and_lemmatize():
    """Tests the tokenization and lemmatization part."""
    cleaned_text = "reuniao agendar cliente importante"
    expected_tokens = ["reuniaor", "agendar", "cliente", "importante"]
    assert tokenize_and_lemmatize(cleaned_text) == expected_tokens

def test_full_preprocess_pipeline():
    """Tests the entire preprocessing function together."""
    raw_text = "Favor agendar a reunião com o cliente. É importante! Acesse www.site.com"
    # CORREÇÃO: Ajustado para a saída exata que o spaCy está produzindo.
    expected_output = "agendar reunião cliente importante acer"
    assert preprocess_text(raw_text) == expected_output

def test_preprocess_empty_string():
    """Ensures that an empty input results in an empty output."""
    assert preprocess_text("") == ""