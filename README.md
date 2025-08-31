# Classificador de E-mails: Produtivo vs. Improdutivo (AutoU Case)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Framework](https://img.shields.io/badge/Framework-FastAPI-green)](https://fastapi.tiangolo.com/)
[![Deployed on Render](https://render.com/images/deploy-to-render-button.svg)](https://auto-u-case-hvieiradev.onrender.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Uma aplicação web completa que classifica e-mails como **Produtivos** ou **Improdutivos**, sugerindo respostas automáticas. Este projeto foi desenhado como uma solução robusta, escalável e pronta para produção para o **Case Prático da AutoU**.

**🚀 Aplicação Online:** [**https://auto-u-case-hvieiradev.onrender.com**](https://auto-u-case-hvieiradev.onrender.com)

## Sumário
- [✨ Principais Funcionalidades](#-principais-funcionalidades)
- [🛠️ Tech Stack](#️-tech-stack)
- [🏛️ Arquitetura da Solução](#️-arquitetura-da-solução)
- [🚀 Setup e Instalação Local](#-setup-e-instalação-local)
- [▶️ Rodando a Aplicação](#️-rodando-a-aplicação)
- [🐳 Docker](#-docker)
- [🧪 Testes Automatizados](#-testes-automatizados)

## ✨ Principais Funcionalidades
- **Classificação de Texto**: Classifica e-mails usando um modelo de Regressão Logística treinado com Scikit-learn e pré-processado com **spaCy**.
- **Frontend Interativo**: Interface para colar texto ou fazer upload de arquivos (`.txt`, `.pdf`).
- **Nível de Confiança**: Exibe a confiança da predição do modelo local.
- **Geração de Resposta**: Utiliza a API da OpenAI (GPT) para sugerir respostas contextuais.

## 🛠️ Tech Stack
- **Backend**: Python, FastAPI, Scikit-learn, spaCy, Uvicorn
- **Frontend**: HTML5, TailwindCSS, JavaScript (Vanilla)
- **Deployment**: Render, Docker

## 🏛️ Arquitetura da Solução
A aplicação segue uma arquitetura cliente-servidor desacoplada:
- **Frontend**: Uma página estática (`frontend/index.html`) que consome a API.
- **Backend**: Uma API RESTful em Python com FastAPI que expõe os endpoints para classificação e geração de texto.
- **Modelo de ML**: Um pipeline do Scikit-learn que encapsula a vetorização (TF-IDF) e a classificação (Regressão Logística).

## 🚀 Setup e Instalação Local

Siga os passos abaixo para configurar e rodar o projeto localmente.

### 1. Pré-requisitos
- Python 3.10+
- Git

### 2. Clone o Repositório
```bash
git clone [https://github.com/hrvieira/auto-u-case.git](https://github.com/hrvieira/auto-u-case.git)
cd auto-u-case
```

### 3. Crie e Ative um Ambiente Virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Instale as Dependências
```bash
pip install -r backend/requirements.txt
```

### 5. Baixe o Modelo do spaCy
```bash
python -m spacy download pt_core_news_sm
```

### 6. Configure as Variáveis de Ambiente
Crie o arquivo `.env` a partir do exemplo e adicione sua chave da API da OpenAI.
```bash
cp .env.example .env
```
Agora, abra o arquivo `.env` e adicione sua chave: `OPENAI_API_KEY="sk-..."`

## ▶️ Rodando a Aplicação

### 1. (Opcional) Treine o Modelo
Para treinar o modelo com os dados mais recentes de `data/examples.csv`, execute:
```bash
python backend/train_classifier.py
```

### 2. Inicie o Servidor
Execute o servidor FastAPI com Uvicorn a partir da **pasta raiz do projeto**:
```bash
uvicorn backend.main:app --reload
```
Acesse a aplicação em [http://127.0.0.1:8000](http://127.0.0.1:8000).

## 🐳 Docker
O projeto está containerizado para facilitar o deploy.

**Construir a imagem:**
```bash
docker build -t email-classifier-app .
```
**Rodar o contêiner:**
```bash
docker run -p 10000:10000 --env-file .env email-classifier-app
```
Acesse a aplicação em [http://localhost:10000](http://localhost:10000).

## 🧪 Testes Automatizados
O projeto conta com uma suíte de testes unitários e de integração. Para executá-los, use o `pytest` na pasta raiz.
```bash
pytest
```