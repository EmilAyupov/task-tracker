from fastapi.testclient import TestClient
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Task
from app.schemas import TaskResponse


def test_delete_existing_task(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        json={"title": "Learn Python"},
    )
    assert response.status_code == 201

    created_task = TaskResponse.model_validate(response.json())
    task_id = created_task.id

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 204
    assert response.content == b""

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 404


def test_delete_nonexistent_task(client: TestClient) -> None:
    response = client.delete("/tasks/999999")

    assert response.status_code == 404


def test_delete_from_db_existing_task(
    client: TestClient,
    db_session: Session,
) -> None:
    response = client.post(
        "/tasks",
        json={"title": "Learn Python"},
    )
    assert response.status_code == 201

    created_task = TaskResponse.model_validate(response.json())
    task_id = created_task.id

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 204
    assert response.content == b""

    db_session.expire_all()

    task = db_session.get(Task, task_id)

    assert task is None


def test_delete_from_db_not_existing_task(
    client: TestClient,
    db_session: Session,
) -> None:
    response = client.post(
        "/tasks",
        json={"title": "Learn Python"},
    )

    assert response.status_code == 201

    count = db_session.scalar(select(func.count()).select_from(Task))

    response = client.delete("/tasks/999999")

    assert response.status_code == 404

    current_count = db_session.scalar(select(func.count()).select_from(Task))

    assert count == current_count


def test_task_with_cleanup(
    client: TestClient,
    task_with_cleanup: int,
) -> None:
    task_id = task_with_cleanup

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
