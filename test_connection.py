
from database.db import get_db_connection

connection = get_db_connection()

if connection.is_connected():
    print("MySQL connected successfully!")

connection.close()
print("Database connection closed.")
