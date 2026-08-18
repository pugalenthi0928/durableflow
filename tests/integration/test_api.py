from uuid import uuid4

from fastapi.testclient import TestClient

from durableflow.main import create_app


def test_create_then_get_job() -> None:
    client = TestClient(create_app())

    create_response = client.post(
        "/v1/jobs",
        json={"filename": "example.txt", "content": "hello durable world"},
        headers={"x-request-id": "request-123"},
    )

    assert create_response.status_code == 201
    assert create_response.headers["x-request-id"] == "request-123"
    created = create_response.json()
    assert created["state"] == "succeeded"
    assert created["result"]["word_count"] == 3

    get_response = client.get(f"/v1/jobs/{created['id']}")
    assert get_response.status_code == 200
    assert get_response.json() == created


def test_invalid_submission_is_rejected() -> None:
    client = TestClient(create_app())

    response = client.post("/v1/jobs", json={"filename": "", "content": ""})

    assert response.status_code == 422


def test_unknown_job_returns_machine_readable_404() -> None:
    client = TestClient(create_app())

    response = client.get(f"/v1/jobs/{uuid4()}")

    assert response.status_code == 404
    assert response.json() == {"detail": "job_not_found"}


def test_new_process_repository_cannot_see_previously_acknowledged_job() -> None:
    first_process = TestClient(create_app())
    created = first_process.post(
        "/v1/jobs",
        json={"filename": "lost.txt", "content": "this state lives only in memory"},
    ).json()

    restarted_process = TestClient(create_app())
    response = restarted_process.get(f"/v1/jobs/{created['id']}")

    assert response.status_code == 404
    assert response.json() == {"detail": "job_not_found"}


def test_health_discloses_memory_storage() -> None:
    client = TestClient(create_app())

    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "storage": "memory"}
