from database import add_menu_item, get_menu

# Add a sample Monday lunch menu
add_menu_item("Monday", "Lunch", "gatte ki sabji")
add_menu_item("Monday", "Lunch", "dal")
add_menu_item("Monday", "Lunch", "rice")
add_menu_item("Monday", "Lunch", "curd")
add_menu_item("Monday", "Lunch", "roti")

# Read Monday lunch
menu = get_menu("Monday", "Lunch")

print("\nMonday Lunch:\n")

for food, in menu:
    print("-", food)