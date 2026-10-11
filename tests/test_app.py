from unittest.mock import patch
from mysql.connector import Error
from services.task_service import TaskValidationError
from app import app


def test_home_route():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json() == {
        "message": "Task Management API is running"
    }


def test_invalid_route():
    client = app.test_client()

    response = client.get("/this-page-does-not-exist")

    assert response.status_code == 404
    assert response.get_json() == {
        "error": "Resource not found"
    }


def test_create_task_without_title():
    client = app.test_client()

    response = client.post(
        "/tasks",
        json={
            "description": "This task has no title",
            "status": "pending"
        }
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Title must not be empty"
    }


def test_create_task_with_invalid_status():
    client = app.test_client()

    response = client.post(
        "/tasks",
        json={
            "title": "Test invalid status",
            "description": "Checking input validation",
            "status": "started"
        }
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Invalid status. Valid statuses: pending, in-progress, completed"
    }


from unittest.mock import patch


def test_get_all_tasks():
    sample_tasks = [
        {
            "id": 1,
            "title": "Learn Python",
            "description": "Practice Flask",
            "status": "pending",
            "created_at": "2026-10-10T19:00:00"
        }
    ]

    with patch(
        "app.get_all_tasks",
        return_value=sample_tasks
    ):
        client = app.test_client()
        response = client.get("/tasks")

    assert response.status_code == 200
    assert response.get_json() == sample_tasks


from unittest.mock import patch

from services.task_service import TaskNotFoundError


def test_get_nonexistent_task():
    with patch(
        "app.get_task_by_id",
        side_effect=TaskNotFoundError("Task not found")
    ):
        client = app.test_client()
        response = client.get("/tasks/99999")

    assert response.status_code == 404
    assert response.get_json() == {
        "error": "Task not found"
    }


def test_get_existing_task():
    sample_task = {
        "id": 1,
        "title": "Learn Python",
        "description": "Practice Flask",
        "status": "pending",
        "created_at": "2026-10-10T19:00:00"
    }

    with patch(
        "app.get_task_by_id",
        return_value=sample_task
    ):
        client = app.test_client()
        response = client.get("/tasks/1")

    assert response.status_code == 200
    assert response.get_json() == sample_task



def test_create_task_successfully():
    sample_task = {
        "id": 10,
        "title": "Learn Flask Testing",
        "description": "Practice automated tests",
        "status": "pending",
        "created_at": "2026-10-11T10:00:00"
    }

    with patch(
        "app.create_task_service",
        return_value=sample_task
    ):
        client = app.test_client()

        response = client.post(
            "/tasks",
            json={
                "title": "Learn Flask Testing",
                "description": "Practice automated tests",
                "status": "pending"
            }
        )

    assert response.status_code == 201
    assert response.get_json() == sample_task


def test_update_task_successfully():
    updated_task = {
        "id": 1,
        "title": "Learn Flask Testing",
        "description": "Updated task description",
        "status": "in-progress",
        "created_at": "2026-10-11T10:00:00"
    }

    with patch(
        "app.update_task_service",
        return_value=updated_task
    ):
        client = app.test_client()

        response = client.put(
            "/tasks/1",
            json={
                "title": "Learn Flask Testing",
                "description": "Updated task description",
                "status": "in-progress"
            }
        )

    assert response.status_code == 200
    assert response.get_json() == updated_task



def test_delete_task_successfully():
    with patch("app.delete_task_service") as mock_delete:
        client = app.test_client()

        response = client.delete("/tasks/1")

    assert response.status_code == 200
    assert response.get_json() == {
        "message": "Task deleted successfully"
    }
    mock_delete.assert_called_once_with(1)


def test_delete_nonexistent_task():
    with patch(
        "app.delete_task_service",
        side_effect=TaskNotFoundError("Task not found")
    ) as mock_delete:
        client = app.test_client()
        response = client.delete("/tasks/99999")

    assert response.status_code == 404
    assert response.get_json() == {
        "error": "Task not found"
    }
    mock_delete.assert_called_once_with(99999)



def test_update_nonexistent_task():
    with patch(
        "app.update_task_service",
        side_effect=TaskNotFoundError("Task not found")
    ) as mock_update:
        client = app.test_client()

        response = client.put(
            "/tasks/99999",
            json={
                "title": "Updated title",
                "status": "pending"
            }
        )

    assert response.status_code == 404
    assert response.get_json() == {
        "error": "Task not found"
    }
    mock_update.assert_called_once_with(
        99999,
        {
            "title": "Updated title",
            "status": "pending"
        }
    )



def test_update_task_with_invalid_status():
    with patch(
        "app.update_task_service",
        side_effect=TaskValidationError(
            "Invalid status. Valid statuses: pending, in-progress, completed"
        )
    ) as mock_update:
        client = app.test_client()

        response = client.put(
            "/tasks/1",
            json={
                "title": "Learn Flask",
                "status": "started"
            }
        )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Invalid status. Valid statuses: pending, in-progress, completed"
    }
    mock_update.assert_called_once_with(
        1,
        {
            "title": "Learn Flask",
            "status": "started"
        }
    )



def test_update_task_with_empty_title():
    with patch(
        "app.update_task_service",
        side_effect=TaskValidationError("Title must not be empty")
    ) as mock_update:
        client = app.test_client()

        response = client.put(
            "/tasks/1",
            json={
                "title": "   ",
                "status": "pending"
            }
        )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Title must not be empty"
    }
    mock_update.assert_called_once_with(
        1,
        {
            "title": "   ",
            "status": "pending"
        }
    )


from mysql.connector import Error

def test_get_all_tasks_database_error():
    with patch(
        "app.get_all_tasks",
        side_effect=Error("Simulated database failure")
    ):
        client = app.test_client()
        response = client.get("/tasks")

    assert response.status_code == 500
    assert response.get_json() == {
        "error": "Failed to retrieve tasks"
    }



def test_create_task_database_error():
    with patch(
        "app.create_task_service",
        side_effect=Error("Simulated database failure")
    ):
        client = app.test_client()

        response = client.post(
            "/tasks",
            json={
                "title": "Learn Flask",
                "description": "Test database error handling",
                "status": "pending"
            }
        )

    assert response.status_code == 500
    assert response.get_json() == {
        "error": "Failed to create task"
    }



def test_update_task_database_error():
    with patch(
        "app.update_task_service",
        side_effect=Error("Simulated database failure")
    ):
        client = app.test_client()

        response = client.put(
            "/tasks/1",
            json={
                "title": "Updated title",
                "status": "in-progress"
            }
        )

    assert response.status_code == 500
    assert response.get_json() == {
        "error": "Failed to update task"
    }


def test_delete_task_database_error():
    with patch(
        "app.delete_task_service",
        side_effect=Error("Simulated database failure")
    ):
        client = app.test_client()
        response = client.delete("/tasks/1")

    assert response.status_code == 500
    assert response.get_json() == {
        "error": "Failed to delete task"
    }
