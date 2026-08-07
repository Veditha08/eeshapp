import sqlite3
from database import DB_NAME

connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()

cursor.execute("""
    DELETE FROM meal_history
    WHERE food = ?
""", ("sambar taste not good",))

connection.commit()
connection.close()

print("Bad test feedback removed!")