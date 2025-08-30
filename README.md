# Case Prático AutoU — Classificador de Emails (Produtivo / Improdutivo)

> **Objetivo:** Aplicação web simples que recebe emails (.txt ou .pdf) ou texto colado, classifica em **Produtivo** ou **Improdutivo** e sugere uma resposta automática.

Este repositório contém uma implementação completa (backend em Python + frontend HTML simples) pensada para o **Case Prático AutoU**. O README abaixo descreve como rodar localmente, treinar o classificador, configurar chaves (OpenAI opcional), testar e fazer deploy.

---

## Conteúdo deste README
- Visão geral da solução  
- Estrutura do repositório  
- Pré-requisitos  
- Instalação passo-a-passo (local)  
- Arquivos de configuração (.env / .env.example / .gitignore)  
- Treinar o modelo local (opcional)  
- Como usar (endpoints e exemplos)  
- Testes  
- Deploy (Render / Heroku / Docker)  
- Entregáveis para submissão ao AutoU  
- Dicas e observações finais

---

## 1. Visão geral da solução

Arquitetura simples:
- **Frontend**: `frontend/index.html` (formulário para upload ou colar texto; consome API).
- **Backend**: `backend/main.py` (FastAPI) — recebe entrada, extrai texto, pré-processa (NLTK), classifica (modelo local scikit-learn ou OpenAI via prompt) e gera resposta (modelo local templates ou OpenAI).
- **Modelo**: pipeline TF-IDF + LogisticRegression (salvo em `backend/models/pipeline.joblib`) — opcional; fallback para OpenAI se `OPENAI_API_KEY` configurada.
- **Deploy**: pode ser hospedado em Render, Heroku, Hugging Face Spaces (adaptando frontend), etc.

---

## 2. Estrutura do repositório (sugerida)

```
auto-u-case/
├─ backend/
│  ├─ main.py
│  ├─ utils_text.py
│  ├─ ai_integration.py
│  ├─ train_classifier.py
│  ├─ requirements.txt
│  └─ models/
│     └─ pipeline.joblib  # gerado pelo treino
├─ frontend/
│  └─ index.html
├─ data/
│  └─ examples.csv
├─ tests/
│  ├─ test_utils.py
│  └─ test_api.py
├─ .env.example
├─ .gitignore
└─ README.md
```

---

## 3. Pré-requisitos

- Python 3.9+ (recomendado 3.10)
- pip
- Git
- (Opcional) Conta OpenAI e `OPENAI_API_KEY`
- (Opcional) Docker

---

## 4. Instalação passo-a-passo (local)

1. **Clone o repositório**
```bash
git clone https://github.com/<seu-usuario>/auto-u-case.git
cd auto-u-case
```

2. **Crie e ative o ambiente virtual**
Linux / macOS:
```bash
python -m venv venv
source venv/bin/activate
```
Windows (PowerShell):
```powershell
python -m venv venv
.env\Scripts\Activate.ps1
```

3. **Instale dependências (backend)**
```bash
pip install -r backend/requirements.txt
```

4. **Baixe recursos do NLTK (uma vez)**
```bash
python - <<PY
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
print("NLTK OK")
PY
```

5. **Crie o arquivo .env a partir do template**
```bash
cp .env.example .env
```
Edite `.env` e adicione sua chave (se usar OpenAI).

6. **(Opcional) Treine o modelo local**
```bash
cd backend
python train_classifier.py
# Isso cria backend/models/pipeline.joblib
cd ..
```

7. **Execute a aplicação**
```bash
cd backend
uvicorn main:app --reload --port 8000
```
Abra: http://localhost:8000  (o endpoint `/` tenta servir o frontend em `../frontend/index.html`)

---

## 5. Arquivos de configuração (.env / .env.example / .gitignore)

**`.env.example`** (NÃO conter chaves reais — use como template):
```env
# Exemplo .env
OPENAI_API_KEY=coloque_sua_chave_aqui
OPENAI_MODEL=gpt-3.5-turbo
MODEL_PATH=./backend/models/pipeline.joblib
```

**`.env`** (NÃO comitar no Git; coloque suas variáveis reais):
```env
OPENAI_API_KEY=sk-xxxxxx_sua_chave_aqui
OPENAI_MODEL=gpt-3.5-turbo
MODEL_PATH=./backend/models/pipeline.joblib
```

**`.gitignore`** - inclua:
```
venv/
.env
*.joblib
*.pkl
__pycache__/
```

---

## 6. Treinar o modelo local (detalhes)

- O script `backend/train_classifier.py` carrega `data/examples.csv`, pré-processa com `backend/utils_text.py`, treina TF-IDF + LogisticRegression e salva em `backend/models/pipeline.joblib`.
- Recomenda-se começar com ~50–200 exemplos e aumentar para melhorar acurácia.
- Exemplo - rodar (na pasta backend):
```bash
python train_classifier.py
```
- O script imprime relatório de classificação (precision/recall/f1) e salva o pipeline.

---

## 7. Como usar (endpoints)

### `POST /api/process`
- Entrada: `multipart/form-data` com **text** (campo) ou **file** (UploadFile .txt ou .pdf).
- Retorna JSON:
```json
{
  "category": "Produtivo",
  "confidence": 0.87,
  "suggested_response": "Texto da resposta sugerida...",
  "preprocessed_excerpt": "trecho pré-processado..."
}
```

#### Exemplo com `curl` (texto):
```bash
curl -X POST "http://localhost:8000/api/process"   -F "text=Olá, preciso atualizar o endereço de cobrança do pedido 1234."
```

#### Exemplo com `curl` (arquivo):
```bash
curl -X POST "http://localhost:8000/api/process"   -F "file=@/caminho/para/email.txt"
```

---

## 8. Frontend (uso rápido)

- Abra `frontend/index.html` em navegador (ou acesse via backend `/` quando estiver servindo).
- Cole o texto do e-mail ou faça upload de um .txt/.pdf e clique em **Processar**.
- O frontend mostra: categoria (com badge), confiança (se disponível) e resposta sugerida.

---

## 9. Testes

- Tests de exemplo em `tests/`.
- Rode:
```bash
pytest -q
```

---

## 10. Deploy (opções recomendadas)

### Deploy no Render (rápido)
1. Faça push no GitHub.
2. Crie um novo **Web Service** no Render, conecte o repo.
3. Configure:
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
4. Defina variável de ambiente `OPENAI_API_KEY` (se for usar).
5. Deploy.

### Deploy no Heroku
1. Adicione `Procfile`:
```
web: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```
2. `git push heroku main` e `heroku config:set OPENAI_API_KEY=sk-...`

### Docker (opcional)
- Build:
```bash
docker build -t autou-case .
```
- Run:
```bash
docker run -p 8000:8000 autou-case
```

---

## 11. Checklist de Entregáveis (para colar no formulário AutoU)

- [ ] Link público do repositório GitHub: `https://github.com/<seu-usuario>/auto-u-case`
- [ ] Link do vídeo demonstrativo (YouTube): `https://youtu.be/<seu-video>`
- [ ] Link da aplicação publicada (Render/Heroku/HuggingFace/...): `https://...`
- [ ] Arquivo `README.md` no repo (este arquivo)
- [ ] `backend/` com código Python e `requirements.txt`
- [ ] `frontend/index.html`
- [ ] `data/examples.csv` com exemplos rotulados
- [ ] Instruções claras no README para rodar local e treinar
- [ ] (Opcional) `backend/models/pipeline.joblib` incluído ou instrução para treinar

---

## 12. Boas práticas e melhorias futuras (sugestões)
- Adicionar feedback do usuário (botão "Corrigir categoria") e persistir correções para re-treinar modelo (active learning).
- Implementar fila + workers (Celery, Redis) para chamadas à OpenAI em alto volume.
- Usar spaCy (pt_core_news_sm) para lematização/NER em pt-BR.
- Fazer fine-tune de um modelo Transformer (se houver muitos dados anotados) para melhorar classificação.
- Implementar OCR (Tesseract) para PDFs digitalizados.

---
