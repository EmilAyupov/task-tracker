from fastapi.testclient import TestClient

from app.models import Task


def test_update_title_task(client: TestClient):
    response = client.post(
        "/tasks",
        json={"title": "Learn Python"},
    )
    assert response.status_code == 201
    task_id = response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"title": "Python Learn"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Python Learn"


def test_update_completed_task(client: TestClient):
    response = client.post(
        "/tasks",
        json={"title": "Learn Python"},
    )
    assert response.status_code == 201
    task_id = response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"completed": True},
    )

    assert response.status_code == 200
    assert response.json()["completed"] is True
    assert response.json()["title"] == "Learn Python"


def test_update_description_task(client: TestClient):
    response = client.post(
        "/tasks",
        json={"title": "Learn Python", "description": "Learn Python"},
    )
    assert response.status_code == 201
    task_id = response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"description": None},
    )
    assert response.status_code == 200
    assert response.json()["description"] is None


def test_update_nonexistent_task(client: TestClient):
    response = client.patch(
        "/tasks/999999",
        json={"title": "Python Learn"},
    )
    assert response.status_code == 404


def test_update_task_with_empty_body(client: TestClient):
    response = client.post(
        "/tasks",
        json={"title": "Learn Python"},
    )
    assert response.status_code == 201
    task_id = response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Learn Python"
    assert response.json()["completed"] is False
    assert response.json()["description"] is None


def test_updated_db_completed_task(client: TestClient, db_session):
    response = client.post(
        "/tasks",
        json={"title": "Learn Python", "completed": False},
    )
    assert response.status_code == 201
    task_id = response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"completed": True},
    )

    db_session.expire_all()

    task = db_session.get(Task, task_id)

    assert task.completed is True


def test_updated_db_fields_task(client: TestClient, db_session):
    response = client.post(
        "/tasks",
        json={"title": "Learn Python", "completed": False},
    )
    assert response.status_code == 201
    task_id = response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"title": "Learn Python Advanced", "completed": True},
    )

    assert response.status_code == 200

    db_session.expire_all()

    task = db_session.get(Task, task_id)

    assert task is not None
    assert task.title == "Learn Python Advanced"
    assert task.completed is True


def test_updated_db_fields_only_one_task(client: TestClient, db_session):
    response = client.post(
        "/tasks",
        json={"title": "Learn Python", "completed": False},
    )
    assert response.status_code == 201
    task_id = response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"completed": True},
    )

    assert response.status_code == 200

    db_session.expire_all()

    task = db_session.get(Task, task_id)

    assert task is not None
    assert task.title == "Learn Python"
    assert task.description is None
    assert task.completed is True


def test_updated_db_fields_only_empty_title_task(client: TestClient, db_session):
    response = client.post(
        "/tasks",
        json={"title": "Learn Python"},
    )
    assert response.status_code == 201
    task_id = response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"title": ""},
    )

    assert response.status_code == 422

    db_session.expire_all()

    task = db_session.get(Task, task_id)

    assert task is not None
    assert task.title == "Learn Python"
