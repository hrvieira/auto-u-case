from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import joblib
import os
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "models" / "email_classifier_pipeline.joblib"
FRONTEND_FILE_PATH = BASE_DIR.parent / "frontend" / "index.html"

from .utils_text import preprocess_text, extract_text_from_pdf_bytes
from .ai_integration import classify_with_openai, generate_response_openai

app = FastAPI(title="AutoU Email Classifier")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = None
try:
    pipeline = joblib.load(MODEL_PATH)
    print(f"Pipeline de classificação carregado com sucesso de '{MODEL_PATH}'.")
except FileNotFoundError:
    print(f"AVISO: Pipeline de modelo não encontrado em '{MODEL_PATH}'. O fallback para OpenAI será usado.")
except Exception as e:
    print(f"Erro ao carregar o pipeline: {e}")

@app.post("/api/process")
async def process_email(text: str = Form(None), file: UploadFile = File(None)):
    if not text and not file:
        return JSONResponse({"error": "É necessário enviar 'text' ou um arquivo."}, status_code=400)

    raw_text = ""
    if file:
        content = await file.read()
        if file.filename and file.filename.lower().endswith('.pdf'):
            raw_text = extract_text_from_pdf_bytes(content)
        else:
            raw_text = content.decode('utf-8', errors='ignore')
    else:
        raw_text = text

    if not raw_text.strip():
        return JSONResponse({"error": "Conteúdo do e-mail está vazio."}, status_code=400)
    
    processed_text = preprocess_text(raw_text)
    category, confidence = None, None

    if pipeline:
        category = pipeline.predict([processed_text])[0]
        probabilities = pipeline.predict_proba([processed_text])[0]
        confidence = float(np.max(probabilities))
    else:
        result = classify_with_openai(raw_text)
        category = result.get('category', 'Erro OpenAI')
        confidence = result.get('confidence', 0.0)
    
    try:
        suggested_response = generate_response_openai(raw_text, category)
    except Exception as e:
        print(f"Erro ao gerar resposta com OpenAI: {e}")
        suggested_response = "Não foi possível gerar uma sugestão no momento."

    return {
        "category": category,
        "confidence": confidence,
        "suggested_response": suggested_response,
        "preprocessed_excerpt": processed_text[:500] + "..."
    }

@app.get("/", response_class=HTMLResponse)
async def read_index():
    """Serve o arquivo frontend."""
    try:
        with open(FRONTEND_FILE_PATH, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse("<h3>Arquivo frontend/index.html não encontrado.</h3>", status_code=404)