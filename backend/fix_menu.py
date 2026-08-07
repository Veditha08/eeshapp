import sqlite3
from database import DB_NAME

connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()

cursor.execute("""
    DELETE FROM weekly_menu
    WHERE day = ?
      AND meal = ?
      AND food = ?
""", ("Saturday", "Lunch", "Dal"))

connection.commit()
connection.close()

print("Removed incorrect Saturday lunch item: Dal")