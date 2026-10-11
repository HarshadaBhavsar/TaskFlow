
from mysql.connector import Error
from database.db import get_db_connection


VALID_STATUSES = ("pending", "in-progress", "completed")


class TaskNotFoundError(Exception):
    pass


class TaskValidationError(Exception):
    pass


def format_task(task):
    """Convert a database task into a JSON-friendly dictionary."""
    if task and task.get("created_at"):
        task["created_at"] = task["created_at"].isoformat(
            timespec="seconds"
        )
    return task


def get_all_tasks():
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, title, description, status, created_at
            FROM tasks
            ORDER BY id
        """)

        tasks = cursor.fetchall()
        return [format_task(task) for task in tasks]

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def get_task_by_id(task_id):
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT id, title, description, status, created_at "
            "FROM tasks WHERE id = %s",
            (task_id,)
        )

        task = cursor.fetchone()

        if task is None:
            raise TaskNotFoundError("Task not found")

        return format_task(task)

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def create_task(data):
    if not isinstance(data, dict):
        raise TaskValidationError("A JSON object is required")

    title = data.get("title")
    description = data.get("description", "")
    status = data.get("status", "pending")

    if not isinstance(title, str) or not title.strip():
        raise TaskValidationError("Title must not be empty")

    if not isinstance(description, str):
        raise TaskValidationError("Description must be a string")

    if not isinstance(status, str) or status not in VALID_STATUSES:
        raise TaskValidationError(
            f"Invalid status. Valid statuses: {', '.join(VALID_STATUSES)}"
        )

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            INSERT INTO tasks (title, description, status)
            VALUES (%s, %s, %s)
            """,
            (title.strip(), description, status)
        )

        task_id = cursor.lastrowid
        connection.commit()

        cursor.execute(
            """
            SELECT id, title, description, status, created_at
            FROM tasks WHERE id = %s
            """,
            (task_id,)
        )

        return format_task(cursor.fetchone())

    except Error:
        if connection and connection.is_connected():
            connection.rollback()
        raise

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def update_task(task_id, data):
    if not isinstance(data, dict):
        raise TaskValidationError("A JSON object is required")

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, title, description, status, created_at
            FROM tasks WHERE id = %s
            """,
            (task_id,)
        )

        task = cursor.fetchone()

        if task is None:
            raise TaskNotFoundError("Task not found")

        title = data.get("title", task["title"])
        description = data.get(
            "description", task["description"] or ""
        )
        status = data.get("status", task["status"])

        if not isinstance(title, str) or not title.strip():
            raise TaskValidationError("Title must not be empty")

        if not isinstance(description, str):
            raise TaskValidationError("Description must be a string")

        if not isinstance(status, str) or status not in VALID_STATUSES:
            raise TaskValidationError(
                f"Invalid status. Valid statuses: {', '.join(VALID_STATUSES)}"
            )

        cursor.execute(
            """
            UPDATE tasks
            SET title = %s, description = %s, status = %s
            WHERE id = %s
            """,
            (title.strip(), description, status, task_id)
        )

        connection.commit()

        cursor.execute(
            """
            SELECT id, title, description, status, created_at
            FROM tasks WHERE id = %s
            """,
            (task_id,)
        )

        return format_task(cursor.fetchone())

    except Error:
        if connection and connection.is_connected():
            connection.rollback()
        raise

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def delete_task(task_id):
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM tasks WHERE id = %s",
            (task_id,)
        )

        if cursor.rowcount == 0:
            raise TaskNotFoundError("Task not found")

        connection.commit()

    except Error:
        if connection and connection.is_connected():
            connection.rollback()
        raise

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
