import allure
import pytest
from fastapi.testclient import TestClient


def test_create_returns_200(client: TestClient):

    response = client.post(
        "/tasks",
        json={"title": "Learn Python"},
    )
    assert response.status_code == 201


def test_tasks_title(client: TestClient):
    response = client.post(
        "/tasks",
        json={"title": "Learn Python"},
    )
    assert response.json()["title"] == "Learn Python"


def test_tasks_uncompleted(client: TestClient):
    response = client.post(
        "/tasks",
        json={"title": "Learn Python"},
    )
    assert response.json()["completed"] is False


def test_create_task_without_title(client: TestClient, attach_response):
    response = client.post(
        "/tasks",
        json={},
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"][1] == "title"

    attach_response(response)

    assert response.json()["detail"][0]["loc"][1] == "title"


def test_create_task_with_whitespace_title(client: TestClient):
    response = client.post(
        "/tasks",
        json={"title": "   "},
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"][1] == "title"


def test_create_task_with_spaces_around_title(client: TestClient):
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
    task_id = response.json()["id"]
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id
    assert response.json()["title"] == "Learn Python"


def test_get_nonexistent_task(client: TestClient):
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
def test_create_task_validation(client, payload, expected_status, attach_response):
    response = client.post("/tasks", json=payload)

    assert response.status_code == expected_status


@allure.title("Создание задачи с корректным заголовком")
@allure.description("Проверяем, что API создаёт задачу и возвращает статус 201")
@allure.severity(allure.severity_level.NORMAL)
def test_create_returns_201(client, attach_response):
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


def test_get_created_task(client, created_task):
    task_id = created_task["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["id"] == task_id
    assert response.json()["title"] == created_task["title"]
