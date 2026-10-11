# TaskFlow — Task Management REST API

A REST API built with Python, Flask, and MySQL to manage tasks. The API supports creating, viewing, updating, and deleting tasks.

## Features

- Create a new task
- Retrieve all tasks
- Retrieve a task by ID
- Update an existing task
- Delete a task
- Validate task titles and statuses
- Handle missing tasks and database errors
- Store database credentials in environment variables
- Test API endpoints using automated tests

## Technologies Used

- Python
- Flask
- MySQL
- MySQL Connector/Python
- python-dotenv
- pytest
- Postman

## Task Statuses

- `pending`
- `in-progress`
- `completed`

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check API status |
| GET | `/tasks` | Retrieve all tasks |
| GET | `/tasks/<id>` | Retrieve a task by ID |
| POST | `/tasks` | Create a task |
| PUT | `/tasks/<id>` | Update a task |
| DELETE | `/tasks/<id>` | Delete a task |

## Example Request

**POST `/tasks`**

```json
{
  "title": "Learn Flask",
  "description": "Build a REST API",
  "status": "pending"
}
```

## Configuration

Create a `.env` file in the project root and configure your MySQL connection settings:

```env
MYSQL_HOST=localhost
MYSQL_USER=task_app
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=task_management
MYSQL_PORT=3306
```

Do not commit your `.env` file or real database credentials to GitHub.

## Run the Project

1. Activate your Python virtual environment.
2. Install the dependencies listed in `requirements.txt`.
3. Configure the `.env` file.
4. Start the application:

```bash
python app.py
```

The API will run locally at `http://127.0.0.1:5000`.

## Run Tests

```bash
python -m pytest -v
```