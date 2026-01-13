from fastapi.testclient import TestClient
from app.main import app
import joblib
import os

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API de Predição Passos Mágicos está online!"}

def test_predict():
    # Carregar as features para criar um input válido
    features_path = os.path.join(os.path.dirname(__file__), "../app/models/features.joblib")
    features = joblib.load(features_path)
    
    # Criar um dicionário com zeros para todas as features
    test_data = {col: 0 for col in features}
    
    response = client.post("/predict", json={"data": test_data})
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert "risk_label" in response.json()
