from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import joblib
import os
from utils_text import preprocess_text, extract_text_from_pdf_bytes
from ai_integration import classify_with_openai, generate_response_openai

app = FastAPI(title="AutoU Email Classifier")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

MODEL_PATH = os.getenv('MODEL_PATH', './models/pipeline.joblib')
model = joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None

@app.post("/api/process")
async def process_email(text: str = Form(None), file: UploadFile = File(None)):
    if not text and not file:
        return JSONResponse({"error": "Enviar 'text' ou um arquivo."}, status_code=400)

    raw_text = ""
    if file:
        content = await file.read()
        if file.filename.lower().endswith('.pdf'):
            raw_text = extract_text_from_pdf_bytes(content)
        else:
            raw_text = content.decode('utf-8', errors='ignore')
    else:
        raw_text = text

    pre = preprocess_text(raw_text)

    category, confidence = None, None
    if model:
        pred = model.predict([pre])[0]
        category = pred
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba([pre])[0]
            classes = model.classes_
            conf_idx = list(classes).index(pred)
            confidence = float(proba[conf_idx])
    else:
        category = classify_with_openai(raw_text)

    try:
        suggested = generate_response_openai(raw_text, category)
    except Exception:
        suggested = (
            "Obrigado pelo contato." if category == "Produtivo"
            else "Agradecemos sua mensagem."
        )

    return {
        "category": category,
        "confidence": confidence,
        "suggested_response": suggested,
        "preprocessed_excerpt": pre[:500]
    }

@app.get("/", response_class=HTMLResponse)
def index():
    try:
        with open("../frontend/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except Exception:
        return HTMLResponse("<h3>Frontend não encontrado</h3>")
