# test_api_requests.py
import requests
import pytest

def test_root_welcome(client, base_url, assert_json, assert_status):
    """Root endpoint should return a welcome message."""
    resp = client.get(base_url)
    assert_status(resp, 200)
    data = assert_json(resp)
    assert "Welcome" in data["message"], f"Expected 'Welcome' in message, got {data}"

def test_translate_found(client, base_url, assert_json, assert_status):
    """Known word + locale -> 200 with translation."""
    resp = client.get(base_url + "translate", params={"query": "apple", "locale": "es-ES"})
    assert_status(resp, 200)
    data = assert_json(resp)
    assert data == {"translation": "manzana"}, f"Unexpected body: {data}"

def test_translate_not_found(client, base_url, assert_json, assert_status):
    """Unknown word -> 404 with error JSON."""
    resp = client.get(base_url + "translate", params={"query": "banana", "locale": "es-ES"})
    assert_status(resp, 404)
    data = assert_json(resp)
    assert data == {"error": "Translation not found"}, f"Unexpected body: {data}"

def test_missing_params_returns_422(client, base_url, assert_json, assert_status):
    """Missing required query params -> 422 validation error."""
    resp = client.get(base_url + "translate")  # no query or locale
    assert_status(resp, 422)
    data = assert_json(resp)
    assert "detail" in data, f"Expected 'detail' in body, got {data}"

@pytest.mark.parametrize("query_variant", ["apple", "APPLE", "ApPlE", "  apple  "])
def test_translate_is_case_insensitive(client, base_url, assert_json, assert_status, query_variant):
    """Different case/whitespace should still return the same translation."""
    resp = client.get(base_url + "translate", params={"query": query_variant, "locale": "es-ES"})
    assert_status(resp, 200)
    data = assert_json(resp)
    assert data == {"translation": "manzana"}, f"Unexpected body: {data}"

def test_unauthorized_without_token(base_url, assert_json, assert_status):
    """Request without token should fail with 401."""
    resp = requests.get(base_url + "translate", params={"query": "apple", "locale": "es-ES"})
    assert_status(resp, 401)
    data = assert_json(resp)
    assert data == {"error": "Unauthorized"}, f"Unexpected body: {data}"

def test_unauthorized_bad_token(base_url, assert_json, assert_status):
    """Bad token should result in 401 Unauthorized."""
    resp = requests.get(
        base_url + "translate",
        params={"query": "apple", "locale": "es-ES"},
        headers={"Authorization": "Bearer WRONG"}
    )
    assert_status(resp, 401)
    data = assert_json(resp)
    assert data == {"error": "Unauthorized"}, f"Unexpected body: {data}"