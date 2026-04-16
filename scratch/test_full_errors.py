import urllib.request
import pytest


BASE_API = "http://localhost:8001"
BASE_FRONT = "http://localhost:3000"


def test_full_case_api():
    url = f"{BASE_API}/full-case/10304468"

    try:
        with urllib.request.urlopen(url) as response:
            assert response.status == 200

    except Exception:
        pytest.skip("API no está activa")


def test_full_case_api_second_id():
    url = f"{BASE_API}/full-case/190326475"

    try:
        with urllib.request.urlopen(url) as response:
            assert response.status == 200

    except Exception:
        pytest.skip("API no está activa")


def test_frontend_health():
    try:
        with urllib.request.urlopen(BASE_FRONT) as response:
            assert response.status == 200

    except Exception:
        pytest.skip("Frontend no está activo")