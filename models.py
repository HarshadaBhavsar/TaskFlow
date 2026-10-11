from datetime import datetime


class Task:
    VALID_STATUSES = ("pending", "in-progress", "completed")

    def __init__(self, task_id, title, description="", status="pending"):
        self.id = task_id
        self.title = title
        self.description = description
        self.status = status
        self.created_at = datetime.now().isoformat(timespec="seconds")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at,
        }