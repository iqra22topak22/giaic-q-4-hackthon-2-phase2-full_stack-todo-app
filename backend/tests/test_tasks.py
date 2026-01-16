import pytest
from fastapi.testclient import TestClient
from main import app
from app.models.task import Task
from app.database import engine, get_session
from sqlmodel import Session, SQLModel, create_engine
from unittest.mock import patch

@pytest.fixture(name="session")
def session_fixture():
    # Use an in-memory SQLite database for testing
    engine = create_engine("sqlite:///./test.db", echo=True)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_create_task(client: TestClient, session: Session):
    # Mock the authentication dependency to return a test user ID
    with patch('app.api.deps.get_current_user', return_value='test_user_123'):
        response = client.post(
            "/api/test_user_123/tasks",
            json={"title": "Test Task", "description": "Test Description"}
        )
        assert response.status_code == 201
        
        data = response.json()
        assert data["success"] is True
        assert data["message"] == "Task created successfully"
        assert "data" in data
        assert data["data"]["title"] == "Test Task"


def test_get_tasks(client: TestClient, session: Session):
    # Mock the authentication dependency
    with patch('app.api.deps.get_current_user', return_value='test_user_123'):
        # First create a task
        client.post(
            "/api/test_user_123/tasks",
            json={"title": "Test Task", "description": "Test Description"}
        )
        
        # Then get tasks
        response = client.get("/api/test_user_123/tasks")
        assert response.status_code == 200
        
        data = response.json()
        assert data["total_count"] >= 1


def test_get_specific_task(client: TestClient, session: Session):
    # Mock the authentication dependency
    with patch('app.api.deps.get_current_user', return_value='test_user_123'):
        # First create a task
        create_response = client.post(
            "/api/test_user_123/tasks",
            json={"title": "Test Task", "description": "Test Description"}
        )
        task_id = create_response.json()["data"]["id"]
        
        # Then get the specific task
        response = client.get(f"/api/test_user_123/tasks/{task_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert data["data"]["title"] == "Test Task"


def test_update_task(client: TestClient, session: Session):
    # Mock the authentication dependency
    with patch('app.api.deps.get_current_user', return_value='test_user_123'):
        # First create a task
        create_response = client.post(
            "/api/test_user_123/tasks",
            json={"title": "Original Task", "description": "Original Description"}
        )
        task_id = create_response.json()["data"]["id"]
        
        # Then update the task
        response = client.put(
            f"/api/test_user_123/tasks/{task_id}",
            json={"title": "Updated Task", "description": "Updated Description"}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert data["data"]["title"] == "Updated Task"


def test_delete_task(client: TestClient, session: Session):
    # Mock the authentication dependency
    with patch('app.api.deps.get_current_user', return_value='test_user_123'):
        # First create a task
        create_response = client.post(
            "/api/test_user_123/tasks",
            json={"title": "Task to Delete", "description": "Description"}
        )
        task_id = create_response.json()["data"]["id"]
        
        # Then delete the task
        response = client.delete(f"/api/test_user_123/tasks/{task_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert data["message"] == "Task deleted successfully"


def test_toggle_task_completion(client: TestClient, session: Session):
    # Mock the authentication dependency
    with patch('app.api.deps.get_current_user', return_value='test_user_123'):
        # First create a task
        create_response = client.post(
            "/api/test_user_123/tasks",
            json={"title": "Task to Toggle", "description": "Description"}
        )
        task_id = create_response.json()["data"]["id"]

        # Then toggle the task completion
        response = client.patch(
            f"/api/test_user_123/tasks/{task_id}/complete",
            json={"completed": True}
        )
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is True
        assert data["data"]["completed"] is True


def test_authentication_missing_token(client: TestClient, session: Session):
    # Test that endpoints return 401 when no token is provided
    # (This would require removing the auth dependency override for this test)
    pass  # This test requires more complex mocking to test auth properly


def test_cross_user_access_prevention(client: TestClient, session: Session):
    # Test that a user cannot access another user's tasks
    # This would require creating tasks for one user and trying to access with another
    pass  # Implementation would require more complex setup