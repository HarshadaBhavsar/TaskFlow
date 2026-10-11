import mysql.connector
from mysql.connector import Error

try:
    db = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="task_app",
        password="Harshada@123",
        database="task_management"
    )

    print("MySQL connected successfully!")

    cursor = db.cursor()
    cursor.execute("SHOW TABLES")

    print("Tables in task_management:")
    for table in cursor.fetchall():
        print(table[0])

    cursor.close()
    db.close()

except Error as e:
    print("Connection failed:", e)