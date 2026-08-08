from datetime import datetime

from database import add_meal_history, get_recent_history


today = datetime.now().strftime("%Y-%m-%d")


print("\n--- EeshApp Feedback ---\n")

print("1. Ate as suggested")
print("2. Didn't like it")
print("3. Ordered outside")
print("4. Didn't eat")
print("5. Something surprised me")

choice = input("\nChoose feedback (1-5): ").strip()


feedback_options = {
    "1": ("ate", "Ate as suggested"),
    "2": ("ate", "Didn't like it"),
    "3": ("ordered_outside", "Ordered outside"),
    "4": ("skipped", "Didn't eat"),
    "5": ("surprised", "Something surprised me"),
}


if choice not in feedback_options:
    print("Invalid choice.")
    exit()


action, feedback = feedback_options[choice]

food = input("What food was this about? ").strip()

details = input(
    "Anything specific about it? (press Enter to skip): "
).strip()


if details:
    feedback = f"{feedback}: {details}"


add_meal_history(
    date=today,
    food=food,
    action=action,
    feedback=feedback
)


print("\nFeedback saved! ✅")

print("\n--- Recent Meal History ---\n")

history = get_recent_history()

for date, food, action, feedback in history:
    print(
        f"{date} | {food} | {action} | {feedback}"
    )