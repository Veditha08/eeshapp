import sqlite3
from database import add_menu_item, DB_NAME, create_database


# Ensure database tables exist
create_database()

# Clear the temporary menu data
connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()
cursor.execute("DELETE FROM weekly_menu")
connection.commit()
connection.close()


weekly_menu = {
    "Monday": {
        "Breakfast": [
            "Aloo Sandwich",
            "Upma",
        ],
        "Lunch": [
            "Aloo Sabji",
            "Kaddu Sabji",
            "Puri",
            "Veg Raita",
        ],
        "Hi-tea": [
            "Maggi",
            "Tea",
        ],
        "Dinner": [
            "Matar Paneer",
            "Rice",
            "Toor Dal",
        ],
    },

    "Tuesday": {
        "Breakfast": [
            "Pav Bhaji",
            "Sprouts",
        ],
        "Lunch": [
            "Kadhi",
            "Dal Sabji",
            "Fry Mirch",
            "Papad",
        ],
        "Hi-tea": [
            "Tea",
            "Namkeen",
            "Semai",
        ],
        "Dinner": [
            "Dosa",
            "Sambar",
            "Chutney",
            "Rice",
            "Moong Dal Halwa",
        ],
    },

    "Wednesday": {
        "Breakfast": [
            "Poha",
            "Jalebi",
            "Omelet",
        ],
        "Lunch": [
            "Chole Bhature",
            "Boondi Raita",
            "Fry Mirch",
        ],
        "Hi-tea": [
            "Tea",
            "Coffee",
            "Bread Pakoda",
        ],
        "Dinner": [
            "Mix Dal Tadka",
            "Methi Aloo",
            "Rice",
        ],
    },

    "Thursday": {
        "Breakfast": [
            "Paneer Bhurji",
            "Paratha",
        ],
        "Lunch": [
            "Black Chana Sabji",
            "Toor Dal",
            "Papad",
            "Lassi",
        ],
        "Hi-tea": [
            "Tea",
            "Bhajiya",
        ],
        "Dinner": [
            "Black Moong Dal",
            "Aloo Peas",
            "Kulcha",
            "Paneer",
        ],
    },

    "Friday": {
        "Breakfast": [
            "Idli",
            "Sambar",
            "Chutney",
        ],
        "Lunch": [
            "Veg Biryani",
            "Onion Raita",
            "Aloo Chhole",
            "Green Chutney",
        ],
        "Hi-tea": [
            "Tea",
            "Samosa",
            "Green Chutney",
            "Red Chutney",
        ],
        "Dinner": [
            "Yellow Dal",
            "Lauki Kofta",
        ],
    },

    "Saturday": {
        "Breakfast": [
            "Onion Paratha",
            "Aloo Sabji",
            "Sprouts",
        ],
        "Lunch": [
            "Rajma Sabji",
            "dahi",
            "Lauki Chana Sabji",
            "Dry Papad",
        ],
        "Hi-tea": [
            "Tea",
            "Coffee",
            "Pasta",
        ],
        "Dinner": [
            "Punjabi Dal Tadka",
            "Aloo Baigan",
            "Any Sweet",
        ],
    },

    "Sunday": {
        "Breakfast": [
            "Uttapam",
            "Chutney",
            "Sambar",
        ],
        "Lunch": [
            "Chana Dal",
            "Dahi",
            "Aloo Paratha",
            "Green Chutney",
        ],
        "Hi-tea": [
            "Tea",
            "Pani Puri",
            "Imli Chutney",
        ],
        "Dinner": [
            "Egg Curry",
            "Paneer Bhurji",
        ],
    },
}


for day, meals in weekly_menu.items():
    for meal, foods in meals.items():
        for food in foods:
            add_menu_item(day, meal, food)


print("Corrected weekly mess menu added successfully!")