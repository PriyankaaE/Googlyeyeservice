from typing import Generator
import pytest
from fastapi.testclient import TestClient
import sys,os
import base64
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.main import app

@pytest.fixture()
def test_data():
    """
        Reads the sample image present in the data folder in Bytes type to mimic the input from FrontEnd 
        It will be passed as function variables to the test function
    """
    with open("data/sample_input.jpg", "rb") as image_file:
            # Read the image as bytes
            img_bytes = image_file.read()
    return base64.b64encode(img_bytes).decode('utf-8')

        
@pytest.fixture()
def client() -> Generator:
    """
        Creates a TestClient and pass it to the test function
    """
    with TestClient(app) as _client:
        yield _client
        app.dependency_overrides = {}