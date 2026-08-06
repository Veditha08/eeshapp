import sqlite3
import os

DB_NAME = os.path.join(os.path.dirname(__file__), "eeshapp.db")


def create_database():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    # Eesha's food preferences
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS food_preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            food TEXT NOT NULL,
            preference TEXT NOT NULL,
            strength TEXT NOT NULL
        )
    """)

    # Eesha's meal history and feedback
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meal_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            food TEXT NOT NULL,
            action TEXT NOT NULL,
            feedback TEXT
        )
    """)

    # Weekly recurring mess menu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weekly_menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day TEXT NOT NULL,
            meal TEXT NOT NULL,
            food TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def add_preference(food, preference, strength):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO food_preferences (food, preference, strength)
        VALUES (?, ?, ?)
    """, (food, preference, strength))

    connection.commit()
    connection.close()


def show_preferences():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT food, preference, strength
        FROM food_preferences
    """)

    preferences = cursor.fetchall()
    connection.close()

    return preferences


def add_menu_item(day, meal, food):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO weekly_menu (day, meal, food)
        VALUES (?, ?, ?)
    """, (day, meal, food))

    connection.commit()
    connection.close()


def get_menu(day, meal):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT food
        FROM weekly_menu
        WHERE day = ? AND meal = ?
    """, (day, meal))

    menu = cursor.fetchall()
    connection.close()

    return menu

def add_meal_history(date, food, action, feedback=None):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO meal_history (date, food, action, feedback)
        VALUES (?, ?, ?, ?)
    """, (date, food, action, feedback))

    connection.commit()
    connection.close()


def get_recent_history(limit=10):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT date, food, action, feedback
        FROM meal_history
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    history = cursor.fetchall()

    connection.close()

    return history


if __name__ == "__main__":
    create_database()
    print("Database ready!")