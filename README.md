# Classificador de E-mails: Produtivo vs. Improdutivo (AutoU Case)


[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Framework](https://img.shields.io/badge/Framework-FastAPI-green)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI/CD](https://img.shields.io/badge/CI/CD-GitHub_Actions-lightgrey)](.github/workflows/ci.yml)

Uma aplicação web completa que classifica e-mails como **Produtivos** ou **Improdutivos**, sugerindo respostas automáticas. Este projeto foi desenhado como uma solução robusta, escalável e pronta para produção para o **Case Prático da AutoU**.

## Sumário

- [✨ Principais Funcionalidades](#-principais-funcionalidades)
- [🏛️ Arquitetura da Solução](#arquitetura-da-solução)
- [🚀 Começando (Ambiente Local)](#-começando-ambiente-local)
- [🔧 Configuração](#-configuração)
- [🧠 Treinando o Modelo de Machine Learning](#-treinando-o-modelo-de-machine-learning)
- [🎮 API e Exemplos de Uso](#-api-e-exemplos-de-uso)
- [🧪 Testes Automatizados](#-testes-automatizados)
- [☁️ Deploy e Escalabilidade](#deploy-e-escalabilidade)
- [💡 Possíveis Melhorias](#-possíveis-melhorias)
- [📜 Licença](#-licença)

---

## ✨ Principais Funcionalidades

* **Processamento Flexível:** Aceita e-mails via upload de arquivos (`.txt`, `.pdf`) ou texto simples.
* **Classificação Híbrida:** Utiliza um modelo local (Scikit-learn) para classificação rápida e de baixo custo, com a opção de fallback para um modelo avançado via API da OpenAI para maior precisão.
* **Geração de Respostas:** Sugere respostas automáticas com base em templates ou, opcionalmente, geradas pela OpenAI.
* **API Robusta:** Backend construído com FastAPI, garantindo alta performance, documentação automática (Swagger UI) e validação de dados.
* **Frontend Simples:** Interface em HTML puro e JavaScript para interação direta com a API, facilitando testes e demonstrações.

---

## 🏛️ Arquitetura da Solução

A solução segue uma arquitetura de microsserviço desacoplada, com um backend servindo uma API RESTful e um frontend agnóstico que a consome.

```mermaid
graph TD
    subgraph "Cliente"
        A[Browser - index.html]
    end

    subgraph "Backend (FastAPI)"
        B(API Endpoint: /api/process)
        C{Lógica de Decisão}
        D[Modelo Local<br>(Scikit-learn)]
        E[API Externa<br>(OpenAI)]
    end

    A -- "Requisição HTTP (Upload ou Texto)" --> B
    B -- "Payload" --> C
    C -- "Se OPENAI_API_KEY existe" --> E
    C -- "Senão" --> D
    D -- "Classificação/Resposta" --> B
    E -- "Classificação/Resposta" --> B
    B -- "Resposta JSON" --> A

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#bbf,stroke:#333,stroke-width:2px
```

* **Frontend (`frontend/`):** Uma página estática (`index.html`) com um formulário que envia os dados para a API via `fetch`. Simples, leve e pode ser facilmente substituído por um framework moderno (React, Vue, etc.).
* **Backend (`backend/`):**
    * `main.py`: Ponto de entrada da aplicação FastAPI. Define o endpoint `/api/process`.
    * `utils_text.py`: Módulo de pré-processamento de texto (limpeza, tokenização, lematização) usando NLTK.
    * `ai_integration.py`: Lógica para interagir tanto com o modelo local (`.joblib`) quanto com a API da OpenAI.
    * `train_classifier.py`: Script para treinar o modelo de classificação (TF-IDF + Logistic Regression) a partir do dataset `data/examples.csv`.
* **Modelo de ML (`backend/models/`):** O `pipeline.joblib` contém o pipeline treinado do Scikit-learn, pronto para ser carregado em produção sem necessidade de retreino.

---

## 🚀 Começando (Ambiente Local)

Siga os passos abaixo para configurar e executar o projeto em sua máquina.

### Pré-requisitos

* Python 3.9+ (recomendado 3.10)
* `pip` e `venv` (geralmente inclusos no Python)
* Git
* (Opcional) Conta na OpenAI para obter uma `OPENAI_API_KEY`.

### Passos de Instalação

1.  **Clone o Repositório:**
    ```bash
    git clone https://github.com/<seu-usuario>/auto-u-case.git
    cd auto-u-case
    ```

2.  **Crie e Ative um Ambiente Virtual:**
    *É uma boa prática isolar as dependências do projeto.*
    ```bash
    # Linux / macOS
    python3 -m venv venv
    source venv/bin/activate

    # Windows (PowerShell)
    python -m venv venv
    .\venv\Scripts\Activate
    ```

3.  **Instale as Dependências:**
    ```bash
    pip install -r backend/requirements.txt
    ```

4.  **Baixe os Recursos do NLTK:**
    *Necessário para o pré-processamento de texto.*
    ```bash
    python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
    ```

5.  **Configure as Variáveis de Ambiente:**
    *Copie o arquivo de exemplo e adicione suas chaves, se aplicável.*
    ```bash
    cp .env.example .env
    ```
    Edite o arquivo `.env` para incluir sua `OPENAI_API_KEY` (opcional).

6.  **(Opcional) Treine o Modelo Local:**
    *Se você modificou `data/examples.csv` ou quer gerar o modelo pela primeira vez.*
    ```bash
    python backend/train_classifier.py
    ```
    Isso criará o arquivo `backend/models/pipeline.joblib`.

7.  **Execute o Servidor de Desenvolvimento:**
    ```bash
    uvicorn backend.main:app --reload --port 8000
    ```
    *A flag `--reload` reinicia o servidor automaticamente após alterações no código, ideal para desenvolvimento.*

    Acesse a aplicação em `http://localhost:8000/` ou a documentação interativa da API em `http://localhost:8000/docs`.

---

## 🔧 Configuração

A configuração da aplicação é feita através de variáveis de ambiente, seguindo os princípios do [12-Factor App](https://12factor.net/config).

* **`.env.example`**: Um template que deve ser versionado no Git. **Nunca** adicione segredos a este arquivo.
    ```env
    # Modelo para configuração. Copie para .env e preencha.
    OPENAI_API_KEY=sua_chave_aqui_se_for_usar
    OPENAI_MODEL=gpt-3.5-turbo
    MODEL_PATH=./backend/models/pipeline.joblib
    ```
* **`.env`**: Arquivo local para desenvolvimento. **Nunca** versione este arquivo no Git. Ele está incluído no `.gitignore` por padrão.
* **`.gitignore`**: Configurado para ignorar arquivos de ambiente, modelos treinados, caches do Python e outras pastas que não devem ser versionadas.

---

## 🧠 Treinando o Modelo de Machine Learning

O script `backend/train_classifier.py` automatiza o processo de treinamento:

1.  Carrega os dados de `data/examples.csv`.
2.  Aplica o pré-processamento de texto definido em `utils_text.py`.
3.  Cria um pipeline do Scikit-learn com `TfidfVectorizer` e `LogisticRegression`.
4.  Treina o modelo e exibe um relatório de classificação (precisão, recall, F1-score).
5.  Salva o pipeline treinado em `backend/models/pipeline.joblib` usando `joblib` para otimização.

Para treinar, basta executar:
```bash
python backend/train_classifier.py
```

---

## 🎮 API e Exemplos de Uso

### Endpoint: `POST /api/process`

Processa um e-mail para classificação e sugestão de resposta.

* **Content-Type:** `multipart/form-data`
* **Parâmetros:**
    * `text` (string, opcional): O corpo do e-mail em texto puro.
    * `file` (file, opcional): Um arquivo `.txt` ou `.pdf` contendo o e-mail.
    * *Pelo menos um dos dois deve ser fornecido.*
* **Resposta de Sucesso (200 OK):**
    ```json
    {
      "category": "Produtivo",
      "confidence": 0.92,
      "suggested_response": "Entendido. Seu endereço de cobrança para o pedido 1234 foi atualizado com sucesso.",
      "preprocessed_excerpt": "olá preciso atualizar endereço cobrança pedido 1234"
    }
    ```

### Exemplos com `curl`

* **Enviando texto:**
    ```bash
    curl -X POST "http://localhost:8000/api/process" \
         -F "text=Olá, gostaria de confirmar o status de entrega do meu pedido #5678."
    ```
* **Enviando um arquivo:**
    ```bash
    curl -X POST "http://localhost:8000/api/process" \
         -F "file=@/path/to/your/email.txt"
    ```

### Exemplo com JavaScript `fetch` (para Frontend)

```javascript
const formData = new FormData();
formData.append('text', 'Preciso da segunda via do meu boleto, por favor.');

fetch('http://localhost:8000/api/process', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```

---

## 🧪 Testes Automatizados

O projeto utiliza `pytest` para testes unitários e de integração.

* `tests/test_utils.py`: Testa as funções de pré-processamento de texto de forma isolada (testes unitários).
* `tests/test_api.py`: Testa o endpoint `/api/process`, simulando requisições e validando as respostas (testes de integração).

Para executar todos os testes:
```bash
pytest -v
```

---

## ☁️ Deploy e Escalabilidade

Esta aplicação foi projetada para ser facilmente "containerizada" e implantada em qualquer provedor de nuvem moderno (AWS, GCP, Azure, Render, Heroku).

### 1. Containerização com Docker

Um `Dockerfile` é fornecido para criar uma imagem leve e otimizada da aplicação.

<details>
<summary>📄 Exemplo de Dockerfile</summary>

```dockerfile
# Stage 1: Build com dependências completas
FROM python:3.10-slim as builder
WORKDIR /app
# Instala dependências de build (se necessário) e do projeto
RUN pip install --upgrade pip
COPY backend/requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt

# Stage 2: Imagem final, mais leve
FROM python:3.10-slim
WORKDIR /app
# Copia as dependências pré-compiladas e o código da aplicação
COPY --from=builder /app/wheels /wheels
COPY backend/ .
COPY data/ ./data
COPY .env.example .
RUN pip install --no-cache /wheels/*
# Expõe a porta e define o comando de execução para produção
EXPOSE 8000
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "backend.main:app", "-b", "0.0.0.0:8000"]
```
</details>

**Comandos Docker:**
```bash
# Construir a imagem
docker build -t email-classifier .
# Rodar o container
docker run -p 8000:8000 -v $(pwd)/.env:/app/.env email-classifier
```
*Servidor de Produção: Note que o Dockerfile utiliza `gunicorn` como servidor WSGI, que é mais robusto para produção do que o servidor de desenvolvimento do `uvicorn`.*

### 2. Integração Contínua e Deploy Contínuo (CI/CD)

Um workflow de GitHub Actions (`.github/workflows/ci.yml`) pode ser configurado para automatizar testes e builds a cada push.

<details>
<summary>📄 Exemplo de Workflow de CI (GitHub Actions)</summary>

```yaml
name: CI Pipeline
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python 3.10
      uses: actions/setup-python@v3
      with:
        python-version: "3.10"
    - name: Install dependencies
      run: |
        pip install -r backend/requirements.txt
        python -m nltk.downloader punkt stopwords wordnet
    - name: Run tests
      run: pytest
```
</details>

### 3. Deploy em Plataformas (Ex: Render)

Plataformas como a Render simplificam o deploy. Você pode conectar seu repositório Git e configurar o serviço usando um arquivo `render.yaml`.

<details>
<summary>📄 Exemplo de render.yaml</summary>

```yaml
services:
  - type: web
    name: email-classifier
    env: python
    plan: free # ou o plano desejado
    buildCommand: |
      pip install -r backend/requirements.txt
      python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
      # Se o modelo não estiver versionado, treine-o aqui:
      # python backend/train_classifier.py
    startCommand: "gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend.main:app -b 0.0.0.0:10000"
    envVars:
      - key: OPENAI_API_KEY
        fromSecret: true # Configure o segredo no dashboard da Render
```
</details>

---

## 💡 Possíveis Melhorias

Esta base sólida pode ser estendida de várias maneiras:

* **Frontend Avançado:** Substituir o `index.html` por uma aplicação em React, Vue ou Svelte para uma experiência de usuário mais rica.
* **Modelos de ML mais sofisticados:** Experimentar modelos baseados em Transformers (ex: BERT, DistilBERT) para classificação de texto, usando bibliotecas como Hugging Face.
* **Cache de Respostas:** Implementar um cache com Redis para armazenar resultados de requisições idênticas, reduzindo a latência e o custo com APIs externas.
* **Monitoramento e Logging:** Integrar ferramentas como Prometheus e Grafana para monitorar a saúde da aplicação e ELK/Loki para logging centralizado.
* **Banco de Dados:** Adicionar um banco de dados (ex: PostgreSQL) para salvar o histórico de e-mails processados e as classificações, permitindo auditoria e retreino contínuo do modelo.

---

## 📜 Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
