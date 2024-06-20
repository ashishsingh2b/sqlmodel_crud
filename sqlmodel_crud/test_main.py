from fastapi.testclient import TestClient
from .main import app,create_db_and_tables
import pytest

client = TestClient(app, raise_server_exceptions=False)


@pytest.fixture(scope="module",autouse=True)
def setup_teardown():
    create_db_and_tables()
    yield

def tests_create_tasks():
    task_data = {"content":"Task Working"}
    response = client.post("/task/",json=task_data)
    assert response.status_code == 200
    assert response.json()["content"] == "Task Working"
    assert "id" in response.json()

def tests_update_task():
    oldtask_data = {"content":"Working"}
    create_respose = client.post("/task/", json=oldtask_data)
    task_id = create_respose.json()["id"]

    updated_task = {"id": task_id, "content":"Update Task"}
    response = client.put("/task/", json=updated_task)
    assert response.status_code == 200
    assert response.json()["content"] == "Update Task"

def test_read_task():
    response =client.get("/task/")
    assert response.status_code == 200
    assert isinstance(response.json(),list)

def test_delete_task():
    task_data = {"content": "Task to delete"}
    response = client.get("/task/",json=task_data)
    task_id = response.json()["id"]

    delete_data = {"id": task_id , "content": "Task to delete"}
    response = client.delete("/task/", json=delete_data)
    assert response.status_code == 200
    assert response.json() == "Task Deleted"



