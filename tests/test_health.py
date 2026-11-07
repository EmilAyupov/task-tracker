def test_health_returns_200(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_health_returns_correct_json(client):
    response = client.get("/health")
    assert response.json() == {"status": "ok"}


def test_health_returns_correct_json_field(client):
    response = client.get("/health")
    assert response.json()["status"] == "ok"


def test_health_post_returns_405(client):
    response = client.post("/health")
    assert response.status_code == 405


def test_unknown_endpoint_returns_404(client):
    response = client.get("/health123")
    assert response.status_code == 404


def test_health_returns_json_content_type(client):
    response = client.get("/health")
    assert "application/json" in response.headers["content-type"]
