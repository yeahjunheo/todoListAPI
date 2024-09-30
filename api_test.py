from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base
from app import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_get_page():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"todos": []}


def test_add_task():
    response = client.post("/add", json={"task": "Test task"})
    assert response.status_code == 200
    assert response.json() == {
        "todos": [
            {
                "id": 1,
                "task": "Test task",
                "status": False,
                "due_date": None,
                "memo": None,
                "steps": [],
            }
        ]
    }


def test_update_status():
    response = client.put("/update/1", json={"task": "Test task", "status": True})
    assert response.status_code == 200
    assert response.json() == {
        "todos": [
            {
                "id": 1,
                "task": "Test task",
                "status": True,
                "due_date": None,
                "memo": None,
                "steps": [],
            }
        ]
    }


def test_update_date():
    response = client.put(
        "/update/1", json={"task": "Test task", "due_date": "2022-12-31"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "todos": [
            {
                "id": 1,
                "task": "Test task",
                "status": True,
                "due_date": "2022-12-31",
                "memo": None,
                "steps": [],
            }
        ]
    }


def test_update_memo():
    response = client.put("/update/1", json={"task": "Test task", "memo": "Test memo"})
    assert response.status_code == 200
    assert response.json() == {
        "todos": [
            {
                "id": 1,
                "task": "Test task",
                "status": True,
                "due_date": "2022-12-31",
                "memo": "Test memo",
                "steps": [],
            }
        ]
    }


def test_add_step():
    response = client.post("/add/steps/1", json={"step": "Test step"})
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "todo_id": 1,
        "status": False,
        "step": "Test step",
    }


def test_update_step_status():
    response = client.put("/update/steps/1", json={"step": "Test step", "status": True})
    assert response.status_code == 200
    assert response.json() == {
        "task": {
            "id": 1,
            "task": "Test task",
            "status": True,
            "due_date": "2022-12-31",
            "memo": "Test memo",
            "steps": [{"id": 1, "todo_id": 1, "status": True, "step": "Test step"}],
        },
        "step": [{"id": 1, "todo_id": 1, "status": True, "step": "Test step"}],
    }


def test_delete_step():
    response = client.delete("/delete/steps/1")
    assert response.status_code == 200
    assert response.json() == {
        "task": {
            "id": 1,
            "task": "Test task",
            "status": True,
            "due_date": "2022-12-31",
            "memo": "Test memo",
            "steps": [],
        },
        "step": [],
    }


def test_search_task():
    response = client.get("/search?search_term=Test")
    assert response.status_code == 200
    assert response.json() == {
        "todos": [
            {
                "id": 1,
                "task": "Test task",
                "status": True,
                "due_date": "2022-12-31",
                "memo": "Test memo",
                "steps": [],
            }
        ]
    }


def test_delete_task():
    response = client.delete("/delete/1")
    assert response.status_code == 200
    assert response.json() == {"todos": []}
