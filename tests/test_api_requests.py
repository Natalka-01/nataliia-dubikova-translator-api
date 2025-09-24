# test_api_requests.py
import requests
import pytest

def test_root_welcome(client, base_url, assert_json):
    """Root endpoint should return a welcome message."""
    resp = client.get(base_url)  
    assert resp.status_code == 200
    data = assert_json(resp)
    assert "Welcome" in data["message"]

def test_translate_found(client, base_url, assert_json):
    """Known word + locale -> 200 with translation."""
    resp = client.get(base_url + "translate", params={"query": "apple", "locale": "es-ES"})
    assert resp.status_code == 200
    data = assert_json(resp)
    assert data == {"translation": "manzana"}

def test_translate_not_found(client, base_url, assert_json):
    """Unknown word -> 404 with error JSON."""
    resp = client.get(base_url + "translate", params={"query": "banana", "locale": "es-ES"})
    assert resp.status_code == 404
    data = assert_json(resp)
    assert data == {"error": "Translation not found"}

def test_missing_params_returns_422(client, base_url, assert_json):
    """Missing required query params -> 422 validation error."""
    resp = client.get(base_url + "translate")  # no query or locale
    assert resp.status_code == 422
    data = assert_json(resp)
    assert "detail" in data  # FastAPI validation error format

@pytest.mark.parametrize("query_variant", ["apple", "APPLE", "ApPlE", "  apple  "])
def test_translate_is_case_insensitive(client, base_url, assert_json, query_variant):
    """Different case/whitespace should still return the same translation."""
    resp = client.get(base_url + "translate", params={"query": query_variant, "locale": "es-ES"})
    assert resp.status_code == 200
    data = assert_json(resp)
    assert data == {"translation": "manzana"}

def test_unauthorized_without_token(base_url, assert_json):
    """Request without token should fail with 401."""
    resp = requests.get(base_url + "translate", params={"query": "apple", "locale": "es-ES"})
    assert resp.status_code == 401
    data = assert_json(resp)
    assert data == {"error": "Unauthorized"}

def test_unauthorized_bad_token(base_url, assert_json):
    """Bad token should result in 401 Unauthorized."""
    resp = requests.get(
        base_url + "translate",
        params={"query": "apple", "locale": "es-ES"},
        headers={"Authorization": "Bearer WRONG"}
    )
    assert resp.status_code == 401
    data = assert_json(resp)
    assert data == {"error": "Unauthorized"}
