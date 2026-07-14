from __future__ import annotations

from fastapi.testclient import TestClient

from app.config import Settings, load_settings
from app.main import create_app


def test_health_returns_200() -> None:
    app = create_app(settings_override=Settings(app_name="Test Backend"))
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "Test Backend"
    assert response.json()["contract_version"] == "v1"


def test_request_id_exists_in_header_and_body() -> None:
    app = create_app(settings_override=Settings())
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.headers["x-request-id"]
    assert response.json()["request_id"] == response.headers["x-request-id"]


def test_missing_auth_on_protected_route_returns_auth_required_envelope() -> None:
    app = create_app(settings_override=Settings(), include_test_routes=True)
    client = TestClient(app)

    response = client.get("/_test/protected")

    assert response.status_code == 401
    payload = response.json()
    assert payload["error"]["code"] == "AUTH_REQUIRED"
    assert payload["error"]["message"]
    assert payload["error"]["field"] is None
    assert payload["error"]["required_action"]
    assert payload["error"]["request_id"] == response.headers["x-request-id"]
    assert payload["error"]["retryable"] is False
    assert payload["error"]["details"] == {}


def test_error_response_matches_contract_shape() -> None:
    app = create_app(settings_override=Settings(), include_test_routes=True)
    client = TestClient(app)

    response = client.get("/_test/protected")
    error = response.json()["error"]

    assert set(error) == {
        "code",
        "message",
        "field",
        "required_action",
        "request_id",
        "retryable",
        "details",
    }


def test_config_can_be_overridden_by_test_environment(monkeypatch) -> None:
    monkeypatch.setenv("BACKEND_APP_NAME", "Env Backend")
    monkeypatch.setenv("BACKEND_ENVIRONMENT", "test")
    monkeypatch.setenv("BACKEND_API_KEY", "test-key")
    monkeypatch.setenv("BACKEND_OWNER_ID", "owner_test")
    monkeypatch.setenv("BACKEND_DATABASE_URL", "sqlite:///./test.db")
    monkeypatch.setenv("BACKEND_PUBLIC_BASE_URL", "http://testserver")
    monkeypatch.setenv("BACKEND_IDEMPOTENCY_COMPLETED_TTL_HOURS", "12")
    monkeypatch.setenv("BACKEND_IDEMPOTENCY_PENDING_LEASE_SECONDS", "30")

    settings = load_settings()

    assert settings.app_name == "Env Backend"
    assert settings.environment == "test"
    assert settings.api_key == "test-key"
    assert settings.owner_id == "owner_test"
    assert settings.database_url == "sqlite:///./test.db"
    assert settings.public_base_url == "http://testserver"
    assert settings.idempotency_completed_ttl_hours == 12
    assert settings.idempotency_pending_lease_seconds == 30


def test_authenticated_route_maps_server_side_owner_id() -> None:
    settings = Settings(api_key="secret", owner_id="owner_from_server")
    app = create_app(settings_override=settings, include_test_routes=True)
    client = TestClient(app)

    response = client.get(
        "/_test/protected",
        headers={"Authorization": "Bearer secret"},
    )

    assert response.status_code == 200
    assert response.json() == {"owner_id": "owner_from_server"}
