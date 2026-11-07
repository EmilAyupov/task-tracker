from collections.abc import Iterator

import allure
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Импортируем модели, чтобы SQLAlchemy зарегистрировал таблицы
# в metadata до выполнения create_all().
from app.database import Base, get_db
from app.main import app

# Отдельная SQLite-база исключительно для тестов.
# Основная база приложения tasks.db не затрагивается.
DATABASE_URL = "sqlite:///./test_tasks.db"


# Создаём движок подключения к тестовой БД.
# check_same_thread=False необходим для работы SQLite
# с TestClient и разными потоками.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)


# Фабрика сессий для взаимодействия с тестовой БД.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# Зависимость FastAPI: приложение будет получать
# сессии именно из тестовой БД, а не из основной.
def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def clean_database(monkeypatch):
    """
    Выполняется автоматически перед каждым тестом.

    1. Удаляет старые таблицы.
    2. Создаёт таблицы заново.
    3. Подменяет подключение FastAPI на тестовую БД.

    monkeypatch автоматически восстановит исходное
    состояние dependency_overrides после теста.
    """

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    monkeypatch.setitem(
        app.dependency_overrides,
        get_db,
        override_get_db,
    )


@pytest.fixture
def db_session(clean_database):
    """
    Предоставляет тесту отдельную SQLAlchemy-сессию.

    После завершения теста сессия автоматически закрывается.
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client() -> Iterator[TestClient]:
    """
    HTTP-клиент для отправки запросов непосредственно
    в FastAPI-приложение без запуска реального сервера.
    """

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def attach_response():
    """
    Возвращает функцию для прикрепления HTTP-запроса
    и HTTP-ответа к Allure-отчёту.
    """

    def _attach_response(response):
        request = response.request

        # Метод и URL запроса.
        allure.attach(
            f"{request.method} {request.url}",
            name="HTTP Request",
            attachment_type=allure.attachment_type.TEXT,
        )

        # Тело запроса прикрепляем, только если оно существует.
        if request.content:
            allure.attach(
                request.content.decode("utf-8"),
                name="Request Body",
                attachment_type=allure.attachment_type.JSON,
            )

        # Тип вложения выбираем по Content-Type ответа.
        content_type = response.headers.get("content-type", "")

        attachment_type = (
            allure.attachment_type.JSON
            if "json" in content_type
            else allure.attachment_type.TEXT
        )

        # Тело ответа. Для 204 оно будет пустым.
        allure.attach(
            response.text,
            name=f"HTTP Response ({response.status_code})",
            attachment_type=attachment_type,
        )

    return _attach_response


@pytest.fixture
def created_task(client, clean_database):

    response = client.post(
        "/tasks",
        json={
            "title": "Test task",
            "description": "Task for automated testing",
        },
    )

    assert response.status_code == 201

    return response.json()


@pytest.fixture
def task_with_cleanup(client):
    # Подготовка
    response = client.post(
        "/tasks",
        json={
            "title": "Test task",
            "description": "Task for automated testing",
        },
    )

    assert response.status_code == 201

    task_id = response.json()["id"]

    try:
        yield task_id

    finally:
        # Очистка гарантированно выполняется после yield
        delete_response = client.delete(f"/tasks/{task_id}")

        assert delete_response.status_code == 204
