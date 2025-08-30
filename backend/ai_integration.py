import os
import openai
from dotenv import load_dotenv

load_dotenv()

OPENAI_KEY = os.getenv('OPENAI_API_KEY')
MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')

if OPENAI_KEY:
    openai.api_key = OPENAI_KEY

def classify_with_openai(text: str) -> str:
    if not OPENAI_KEY:
        raise RuntimeError("OPENAI_API_KEY não configurada.")
    prompt = (
        "Classifique o seguinte e-mail em 'Produtivo' ou 'Improdutivo'.\n\n"
        f"E-mail:\n\"\"\"{text}\"\"\"\n\nResposta:"
    )
    resp = openai.ChatCompletion.create(
        model=MODEL,
        messages=[{"role":"user","content":prompt}],
        max_tokens=16,
        temperature=0
    )
    out = resp['choices'][0]['message']['content'].strip()
    if 'produt' in out.lower():
        return 'Produtivo'
    elif 'improdut' in out.lower():
        return 'Improdutivo'
    return out

def generate_response_openai(text: str, category: str) -> str:
    if not OPENAI_KEY:
        raise RuntimeError("OPENAI_API_KEY não configurada.")
    template = (
        f"O e-mail recebido é:\n\n\"\"\"{text}\"\"\"\n\n"
        f"A categoria foi: {category}.\n\n"
        "Escreva uma resposta profissional curta e cordial. "
        "Se for 'Produtivo', inclua próximos passos; se 'Improdutivo', apenas agradeça."
    )
    resp = openai.ChatCompletion.create(
        model=MODEL,
        messages=[{"role":"user","content":template}],
        max_tokens=300,
        temperature=0.3
    )
    return resp['choices'][0]['message']['content'].strip()