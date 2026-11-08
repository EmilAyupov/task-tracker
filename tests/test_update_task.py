from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import Task
from app.schemas import TaskResponse


def test_update_title_task(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        json={"title": "Learn Python"},
    )
    assert response.status_code == 201
    created_task = TaskResponse.model_validate_json(response.content)
    task_id = created_task.id

    response = client.patch(
        f"/tasks/{task_id}",
        json={"title": "Python Learn"},
    )
    assert response.status_code == 200
    updated_task = TaskResponse.model_validate_json(response.content)

    assert updated_task.title == "Python Learn"


def test_update_completed_task(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        json={"title": "Learn Python"},
    )
    assert response.status_code == 201
    task_id = TaskResponse.model_validate_json(response.content).id

    response = client.patch(
        f"/tasks/{task_id}",
        json={"completed": True},
    )

    assert response.status_code == 200
    updated_task = TaskResponse.model_validate_json(response.content)

    assert updated_task.completed is True
    assert updated_task.title == "Learn Python"


def test_update_description_task(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        json={"title": "Learn Python", "description": "Learn Python"},
    )
    assert response.status_code == 201
    task_id = TaskResponse.model_validate_json(response.content).id

    response = client.patch(
        f"/tasks/{task_id}",
        json={"description": None},
    )
    assert response.status_code == 200
    updated_task = TaskResponse.model_validate_json(response.content)

    assert updated_task.description is None


def test_update_nonexistent_task(client: TestClient) -> None:
    response = client.patch(
        "/tasks/999999",
        json={"title": "Python Learn"},
    )
    assert response.status_code == 404


def test_update_task_with_empty_body(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        json={"title": "Learn Python"},
    )
    assert response.status_code == 201
    task_id = TaskResponse.model_validate_json(response.content).id

    response = client.patch(
        f"/tasks/{task_id}",
        json={},
    )
    assert response.status_code == 200
    updated_task = TaskResponse.model_validate_json(response.content)

    assert updated_task.title == "Learn Python"
    assert updated_task.completed is False
    assert updated_task.description is None


def test_updated_db_completed_task(
    client: TestClient,
    db_session: Session,
) -> None:
    response = client.post(
        "/tasks",
        json={"title": "Learn Python", "completed": False},
    )
    assert response.status_code == 201
    task_id = TaskResponse.model_validate_json(response.content).id

    response = client.patch(
        f"/tasks/{task_id}",
        json={"completed": True},
    )
    assert response.status_code == 200

    db_session.expire_all()

    task = db_session.get(Task, task_id)

    assert task is not None
    assert task.completed is True


def test_updated_db_fields_task(
    client: TestClient,
    db_session: Session,
) -> None:
    response = client.post(
        "/tasks",
        json={"title": "Learn Python", "completed": False},
    )
    assert response.status_code == 201
    task_id = TaskResponse.model_validate_json(response.content).id

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


def test_updated_db_fields_only_one_task(
    client: TestClient,
    db_session: Session,
) -> None:
    response = client.post(
        "/tasks",
        json={"title": "Learn Python", "completed": False},
    )
    assert response.status_code == 201
    task_id = TaskResponse.model_validate_json(response.content).id

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


def test_updated_db_fields_only_empty_title_task(
    client: TestClient,
    db_session: Session,
) -> None:
    response = client.post(
        "/tasks",
        json={"title": "Learn Python"},
    )
    assert response.status_code == 201
    task_id = TaskResponse.model_validate_json(response.content).id

    response = client.patch(
        f"/tasks/{task_id}",
        json={"title": ""},
    )

    assert response.status_code == 422

    db_session.expire_all()

    task = db_session.get(Task, task_id)

    assert task is not None
    assert task.title == "Learn Python"


def test_update_task_with_null_title(
    client: TestClient,
    created_task: TaskResponse,
) -> None:
    response = client.patch(
        f"/tasks/{created_task.id}",
        json={"title": None},
    )

    assert response.status_code == 422
    assert response.json()["detail"] == "title cannot be null"


def test_update_task_with_null_completed(
    client: TestClient,
    created_task: TaskResponse,
) -> None:
    response = client.patch(
        f"/tasks/{created_task.id}",
        json={"completed": None},
    )

    assert response.status_code == 422
    assert response.json()["detail"] == "completed cannot be null"
