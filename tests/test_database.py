import pytest

from app import database


def test_get_db_closes_session(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeSession:
        closed: bool = False

        def close(self) -> None:
            self.closed = True

    fake_session = FakeSession()

    def create_fake_session() -> FakeSession:
        return fake_session

    monkeypatch.setattr(
        database,
        "SessionLocal",
        create_fake_session,
    )

    db_generator = database.get_db()

    db = next(db_generator)

    assert db is fake_session
    assert fake_session.closed is False

    db_generator.close()

    assert fake_session.closed is True
