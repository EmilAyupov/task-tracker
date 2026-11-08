from collections.abc import Callable

import pytest
from fastapi.testclient import TestClient
from httpx2 import Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Task


@pytest.mark.parametrize(
    "payload, expected_status",
    [
        ({"title": ""}, 422),
        ({"title": "   "}, 422),
        ({}, 422),
        ({"title": 123}, 422),
        ({"title": None}, 422),
    ],
    ids=[
        "empty_title",
        "whitespace_title",
        "missing_title",
        "wrong_title_type",
        "null_title",
    ],
)
def test_create_task_validation(
    client: TestClient,
    payload: dict[str, object],
    expected_status: int,
    attach_response: Callable[[Response], None],
) -> None:
    response = client.post("/tasks", json=payload)

    attach_response(response)

    assert response.status_code == expected_status
    assert "detail" in response.json()
    assert isinstance(response.json()["detail"], list)


def test_invalid_task_is_not_saved(
    client: TestClient,
    db_session: Session,
) -> None:
    response = client.post("/tasks", json={"title": ""})

    assert response.status_code == 422

    tasks = db_session.scalars(select(Task)).all()

    assert tasks == []
