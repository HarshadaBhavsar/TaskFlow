from errors import register_error_handlers
from flask import Flask, jsonify, request
from mysql.connector import Error

from services.task_service import (
    get_all_tasks,
    get_task_by_id,
    create_task as create_task_service,
    update_task as update_task_service,
    delete_task as delete_task_service,
    TaskNotFoundError,
    TaskValidationError,
)

app = Flask(__name__)
register_error_handlers(app)


@app.route("/")
def home():
    return jsonify({
        "message": "Task Management API is running"
    }), 200


@app.route("/tasks", methods=["GET"])
def get_tasks():
    try:
        tasks = get_all_tasks()
        return jsonify(tasks), 200

    except Error:
        app.logger.exception("Failed to retrieve tasks")
        return jsonify({"error": "Failed to retrieve tasks"}), 500


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    try:
        task = get_task_by_id(task_id)
        return jsonify(task), 200

    except TaskNotFoundError:
        return jsonify({"error": "Task not found"}), 404

    except Error:
        app.logger.exception("Failed to retrieve task")
        return jsonify({"error": "Failed to retrieve task"}), 500


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "A JSON object is required"}), 400

    try:
        task = create_task_service(data)
        return jsonify(task), 201

    except TaskValidationError as error:
        return jsonify({"error": str(error)}), 400

    except Error:
        app.logger.exception("Failed to create task")
        return jsonify({"error": "Failed to create task"}), 500


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "A JSON object is required"}), 400

    try:
        task = update_task_service(task_id, data)
        return jsonify(task), 200

    except TaskNotFoundError:
        return jsonify({"error": "Task not found"}), 404

    except TaskValidationError as error:
        return jsonify({"error": str(error)}), 400

    except Error:
        app.logger.exception("Failed to update task")
        return jsonify({"error": "Failed to update task"}), 500


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    try:
        delete_task_service(task_id)

        return jsonify({
            "message": "Task deleted successfully"
        }), 200

    except TaskNotFoundError:
        return jsonify({"error": "Task not found"}), 404

    except Error:
        app.logger.exception("Failed to delete task")
        return jsonify({"error": "Failed to delete task"}), 500


if __name__ == "__main__":
    app.run(debug=True)
