import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "Swagger UI" in response.json()["message"]

def test_cad_endpoint_file_not_found():
    response = client.post("/api/cad/process-cad", json={"file_path": "non_existent_file.SLDPRT"})
    assert response.status_code == 404
    assert response.json()["detail"] == "CAD file not found on server."

def test_ml_predict_endpoint():
    # Provide dummy sequential data
    dummy_sequence = [[0.1, 0.2, 0.3, 0.4] for _ in range(50)]
    
    response = client.post("/api/ml/predict-rul", json={"sequence_data": dummy_sequence})
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "remaining_useful_life_hours" in data
