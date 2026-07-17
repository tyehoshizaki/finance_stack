import pytest

from app.databases.database import get_db

# Database Setup and Teardown Test

# test database is clean between tests
def test_database_is_clean_between_tests(client):
    response = client.get("/transactions/")
    assert response.status_code == 200
    assert response.json()["items"] == []

def test_get_db_yields_and_closes_session(monkeypatch):
    class FakeSession:
        def __init__(self):
            self.closed = False

        def close(self):
            self.closed = True

    fake_session = FakeSession()

    monkeypatch.setattr(
        "app.databases.database.SessionLocal",
        lambda: fake_session,
    )

    db_generator = get_db()

    yielded_session = next(db_generator)

    assert yielded_session is fake_session
    assert fake_session.closed is False

    with pytest.raises(StopIteration):
        next(db_generator)

    assert fake_session.closed is True