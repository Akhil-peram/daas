import pytest
from fastapi.testclient import TestClient
from main import app
import io
import pandas as pd

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Dashboard as a Service API is running"}

def test_upload_csv():
    # Create a dummy CSV file
    data = "name,age\nAlice,30\nBob,25"
    file = io.BytesIO(data.encode("utf-8"))
    
    response = client.post(
        "/api/upload",
        files={"file": ("test.csv", file, "text/csv")}
    )
    
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["filename"] == "test.csv"
    assert "columns" in json_response
    assert "row_count" in json_response
    assert json_response["row_count"] == 2
    assert "name" in json_response["columns"]
    assert "age" in json_response["columns"]

def test_upload_invalid_type():
    file = io.BytesIO(b"dummy content")
    
    response = client.post(
        "/api/upload",
        files={"file": ("test.txt", file, "text/plain")}
    )
    
    assert response.status_code == 200
    assert "error" in response.json()
    assert "Unsupported file type" in response.json()["error"]
