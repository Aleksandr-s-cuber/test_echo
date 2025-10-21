import requests
import json
import pytest
from requests.exceptions import RequestException

BASE_URL = "https://postman-echo.com"  

@pytest.fixture(scope="session")
def base_url():
    return "https://postman-echo.com"

@pytest.fixture(scope="session")
def http_session():
    session = requests.Session()
    yield session
    session.close()

def test_get_with_params(base_url, http_session):
    """Тест GET-запроса с параметрами."""
    params = {"key1": "value1", "key2": "value2"}
    try:
        response = http_session.get(f"{base_url}/get", params=params)
        response.raise_for_status()
    except RequestException as e:
        pytest.fail(f"Request failed: {e}")

    assert response.status_code == 200
    data = response.json()
    assert "args" in data
    assert data["args"] == params

def test_get_param_encoding(base_url, http_session):
    """Тест кодирования параметров GET-запроса."""
    params = {"query": "some value with spaces"}
    try:
        response = http_session.get(f"{base_url}/get", params=params)
        response.raise_for_status()  # Проверяем статус код
    except RequestException as e:
        pytest.fail(f"Request failed: {e}")

    assert response.status_code == 200
    data = response.json()
    assert "args" in data
    assert data["args"]["query"] == "some value with spaces"

@pytest.mark.parametrize(
    "payload",
    [
        {"key1": "value1", "key2": "value2"},
        {}
    ]
)
def test_post_json(base_url, http_session, payload):
    """Тест POST-запроса с JSON-телом."""
    headers = {'Content-Type': 'application/json'}
    try:
        response = http_session.post(f"{base_url}/post", data=json.dumps(payload), headers=headers)
        response.raise_for_status()
    except RequestException as e:
        pytest.fail(f"Request failed: {e}")

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert data["data"] == payload

def test_post_form_data(base_url, http_session):
    """Тест POST-запроса с данными формы."""
    payload = {"key1": "value1", "key2": "value2"}
    try:
        response = http_session.post(f"{base_url}/post", data=payload)
        response.raise_for_status()
    except RequestException as e:
        pytest.fail(f"Request failed: {e}")

    assert response.status_code == 200
    data = response.json()
    assert "form" in data
    assert data["form"] == payload

def test_custom_header(base_url, http_session):
    """Тест отправки пользовательского заголовка."""
    headers = {"X-Custom-Header": "my-custom-value"}
    try:
        response = http_session.get(f"{base_url}/get", headers=headers)
        response.raise_for_status() # Проверяем статус код
    except RequestException as e:
        pytest.fail(f"Request failed: {e}")

    assert response.status_code == 200
    data = response.json()
    assert "headers" in data
    assert data["headers"]["x-custom-header"] == "my-custom-value"