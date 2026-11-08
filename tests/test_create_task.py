from collections.abc import Callable
from typing import TypeVar, cast

import allure
import pytest
from fastapi.testclient import TestClient
from httpx2 import Response

from app.schemas import TaskResponse

F = TypeVar("F", bound=Callable[..., object])


def typed_allure_title(value: str) -> Callable[[F], F]:
    factory = cast(
        Callable[[str], Callable[[F], F]],
        getattr(allure, "title"),  # noqa: B009
    )
    return factory(value)


def typed_allure_description(value: str) -> Callable[[F], F]:
    factory = cast(
        Callable[[str], Callable[[F], F]],
        getattr(allure, "description"),  # noqa: B009
    )
    return factory(value)


def typed_allure_severity(value: str) -> Callable[[F], F]:
    factory = cast(
        Callable[[str], Callable[[F], F]],
        getattr(allure, "severity"),  # noqa: B009
    )
    return factory(value)


def test_create_returns_200(client: TestClient) -> None:

    response = client.post(
        "/tasks",
        json={"title": "Learn Python"},
    )
    assert response.status_code == 201


def test_tasks_title(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        json={"title": "Learn Python"},
    )
    assert response.json()["title"] == "Learn Python"


def test_tasks_uncompleted(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        json={"title": "Learn Python"},
    )
    assert response.json()["completed"] is False


def test_create_task_without_title(
    client: TestClient, attach_response: Callable[[Response], None]
):
    response = client.post(
        "/tasks",
        json={},
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"][1] == "title"

    attach_response(response)

    assert response.json()["detail"][0]["loc"][1] == "title"


def test_create_task_with_whitespace_title(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        json={"title": "   "},
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"][1] == "title"


def test_create_task_with_spaces_around_title(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        json={"title": "  Learn Python  "},
    )
    assert response.status_code == 201
    assert response.json()["title"] == "  Learn Python  "


def test_get_existing_task(client: TestClient):
    response = client.post(
        "/tasks",
        json={"title": "Learn Python"},
    )

    created_task = TaskResponse.model_validate(response.json())
    task_id = created_task.id

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["id"] == task_id
    assert response.json()["title"] == "Learn Python"


def test_get_nonexistent_task(client: TestClient) -> None:
    response = client.get("/tasks/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


@pytest.mark.parametrize(
    "payload, expected_status",
    [
        ({"title": "Learn Python"}, 201),
        ({"title": ""}, 422),
        ({"title": "   "}, 422),
        ({}, 422),
    ],
    ids=[
        "valid_title",
        "empty_title",
        "whitespace_title",
        "missing_title",
    ],
)
def test_create_task_validation(
    client: TestClient,
    payload: dict[str, str],
    expected_status: int,
    attach_response: Callable[[Response], None],
) -> None:
    response = client.post("/tasks", json=payload)

    attach_response(response)

    assert response.status_code == expected_status


@typed_allure_title("Создание задачи с корректным заголовком")
@typed_allure_description("Проверяем, что API создаёт задачу и возвращает статус 201")
@typed_allure_severity(allure.severity_level.NORMAL)
def test_create_returns_201(
    client: TestClient, attach_response: Callable[[Response], None]
):
    with allure.step("Отправляем запрос на создание задачи"):
        response = client.post(
            "/tasks",
            json={"title": "Learn Python"},
        )

    attach_response(response)

    with allure.step("Проверяем статус-код ответа"):
        assert response.status_code == 201
        allure.attach(
            response.text,
            name="HTTP Response",
            attachment_type=allure.attachment_type.JSON,
        )


def test_get_created_task(
    client: TestClient,
    created_task: TaskResponse,
) -> None:
    task_id = created_task.id

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["id"] == task_id
    assert response.json()["title"] == created_task.title
