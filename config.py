
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_USER = os.getenv("MYSQL_USER", "task_app")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "task_management")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))

    @classmethod
    def validate(cls):
        if not cls.MYSQL_PASSWORD:
            raise ValueError(
                "MYSQL_PASSWORD is missing. Check your .env file."
            )
