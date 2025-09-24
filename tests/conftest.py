import pytest, requests

BASE_URL = "http://127.0.0.1:8000/"

@pytest.fixture(scope="session")
def base_url():
    """Return the base URL for the API."""
    return BASE_URL

@pytest.fixture(scope="module")
def client():
    """Reusable HTTP client with a fake auth token in headers."""
    s = requests.Session()

    # Fake token 
    fake_token = "test-fake-jwt-token"

    # Add headers to every request made by this session
    s.headers.update({
        "Authorization": f"Bearer {fake_token}",
        "Content-Type": "application/json"
    })

    yield s
    s.close()


@pytest.fixture
def assert_json():
    """Check response is JSON and return parsed dict."""
    def _assert_json(resp):
        content_type = resp.headers.get("Content-Type", "")
        assert content_type.startswith("application/json"), \
            f"Expected JSON, got {content_type}"
        return resp.json()
    return _assert_json