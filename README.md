# Classificador de E-mails: Produtivo vs. Improdutivo (AutoU Case)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Framework](https://img.shields.io/badge/Framework-FastAPI-green)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI/CD](https://img.shields.io/badge/CI/CD-GitHub_Actions-lightgrey)](.github/workflows/ci.yml)

Uma aplicação web completa que classifica e-mails como **Produtivos** ou **Improdutivos**, sugerindo respostas automáticas. Este projeto foi desenhado como uma solução robusta, escalável e pronta para produção para o **Case Prático da AutoU**.

## Sumário
- [✨ Principais Funcionalidades](#-principais-funcionalidades)
- [🏛️ Arquitetura da Solução](#️-arquitetura-da-solução)
- [🚀 Começando (Ambiente Local)](#-começando-ambiente-local)
- [🧠 Treinando o Modelo de Machine Learning](#-treinando-o-modelo-de-machine-learning)
- [▶️ Rodando a Aplicação](#️-rodando-a-aplicação)
- [🐳 Docker](#-docker)
- [🧪 Testes Automatizados](#-testes-automatizados)
- [💡 Possíveis Melhorias](#-possíveis-melhorias)

## ✨ Principais Funcionalidades
- **Classificação de Texto**: Classifica o texto de e-mails usando um modelo de Regressão Logística treinado com Scikit-learn e pré-processado com spaCy.
- **Frontend Interativo**: Interface simples para colar texto ou fazer upload de arquivos (`.txt`, `.pdf`).
- **Nível de Confiança**: Exibe a confiança da predição do modelo local.
- **Geração de Resposta**: Utiliza a API da OpenAI (GPT) para sugerir respostas contextuais.
- **API Backend**: Construído com FastAPI, garantindo alta performance e documentação automática.

## 🏛️ Arquitetura da Solução
A aplicação segue uma arquitetura cliente-servidor desacoplada:
- **Frontend**: Uma página estática (`index.html`) que consome a API.
- **Backend**: Uma API RESTful em Python com FastAPI que expõe os endpoints para classificação e geração de texto.
- **Modelo de ML**: Um pipeline do Scikit-learn que encapsula a vetorização (TF-IDF) e a classificação (Regressão Logística).

## 🚀 Começando (Ambiente Local)

Siga os passos abaixo para configurar e rodar o projeto localmente.

### 1. Pré-requisitos
- [Python 3.10+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)

### 2. Clone o Repositório
```bash
git clone [https://github.com/seu-usuario/auto-u-case.git](https://github.com/seu-usuario/auto-u-case.git)
cd auto-u-case
```

### 3. Crie e Ative um Ambiente Virtual
É uma boa prática isolar as dependências do projeto.

```bash
# Para Windows
python -m venv venv
venv\Scripts\activate

# Para macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Instale as Dependências
```bash
pip install -r backend/requirements.txt
```

### 5. Baixe o Modelo do spaCy
O projeto utiliza o spaCy para processamento de texto em português. Baixe o modelo necessário.

```bash
python -m spacy download pt_core_news_sm
```

### 6. Configure as Variáveis de Ambiente
Crie o arquivo `.env` a partir do exemplo e adicione sua chave da API da OpenAI.

```bash
cp .env.example .env
```
Agora, abra o arquivo `.env` e adicione sua chave:
```
OPENAI_API_KEY="sk-..."
```

## 🧠 Treinando o Modelo de Machine Learning

Para garantir que o modelo de ML esteja atualizado com os dados mais recentes de `data/examples.csv`, execute o script de treinamento.

```bash
python backend/train_classifier.py
```
Isso irá gerar ou atualizar o arquivo `backend/models/email_classifier_pipeline.joblib`.

## ▶️ Rodando a Aplicação

### 1. Inicie o Servidor
Execute o servidor FastAPI com Uvicorn a partir da **pasta raiz do projeto**.

```bash
uvicorn backend.main:app --reload
```
O `--reload` faz com que o servidor reinicie automaticamente após alterações no código.

### 2. Acesse a Aplicação
Abra seu navegador e acesse o endereço: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## 🐳 Docker
O projeto também inclui um `Dockerfile` para facilitar o build e deploy da aplicação em contêineres.

**Construir a imagem:**
```bash
docker build -t email-classifier-app .
```
**Rodar o contêiner:**
```bash
docker run -p 8000:8000 --env-file .env email-classifier-app
```

## 🧪 Testes Automatizados
O projeto conta com testes unitários para garantir a qualidade do código. Para executá-los, use o `pytest`.

```bash
pytest
```
## 💡 Possíveis Melhorias
Esta base sólida pode ser estendida de várias maneiras:
* **Frontend Avançado:** Substituir o `index.html` por uma aplicação em React, Vue ou Svelte.
* **Modelos de ML mais sofisticados:** Experimentar modelos baseados em Transformers (ex: BERT) com Hugging Face.
* **Cache de Respostas:** Implementar um cache com Redis para reduzir a latência e o custo com APIs externas.