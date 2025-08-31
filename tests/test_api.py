import sys
import os
import io
from fastapi.testclient import TestClient
import pytest

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa o 'app' DEPOIS de ajustar o path
from backend.main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_dependencies(monkeypatch):
    """
    Este fixture usa monkeypatch para substituir nossas dependências externas (ML e OpenAI)
    por funções falsas (mocks) que retornam valores controlados.
    """
    class MockPipeline:
        def predict(self, data):
            return ["Produtivo"]

        def predict_proba(self, data):
            return [[0.05, 0.95]] # Probabilidade de 95% para 'Produtivo'

    monkeypatch.setattr("backend.main.pipeline", MockPipeline())

    def mock_generate_response(text, category):
        return f"Mock response for category '{category}'."

    monkeypatch.setattr("backend.main.generate_response_openai", mock_generate_response)

def test_process_with_text_input():
    """Tests the API endpoint with a simple text input."""
    response = client.post("/api/process", data={"text": "Por favor, revise o relatório."})
    assert response.status_code == 200
    data = response.json()
    assert data["category"] == "Produtivo"
    assert data["confidence"] == 0.95

def test_process_with_file_upload():
    """Tests the API endpoint with a file upload."""
    file_content = b"Este e um email de teste."
    mock_file = ("test.txt", io.BytesIO(file_content), "text/plain")
    response = client.post("/api/process", files={"file": mock_file})
    assert response.status_code == 200
    data = response.json()
    assert data["category"] == "Produtivo"

def test_process_with_no_input():
    """Tests the API's error handling when no input is provided."""
    response = client.post("/api/process")
    assert response.status_code == 400
    # CORREÇÃO: Verificando a chave 'error' que sua API realmente retorna.
    assert "necessário enviar 'text' ou um arquivo" in response.json()["error"]