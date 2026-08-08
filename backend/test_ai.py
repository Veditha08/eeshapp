import tinker
from datetime import datetime
from tinker_cookbook import renderers

from database import show_preferences, get_menu, get_recent_history


# -----------------------------------
# 1. Find today's day and meal
# -----------------------------------

now = datetime.now()

day = now.strftime("%A")
hour = now.hour

if 6 <= hour < 11:
    meal = "Breakfast"
elif 11 <= hour < 16:
    meal = "Lunch"
elif 16 <= hour < 18:
    meal = "Hi-tea"
else:
    meal = "Dinner"


# -----------------------------------
# 2. Get Eesha's preferences
# -----------------------------------

preferences = show_preferences()

preferences_text = "\n".join(
    [
        f"- {food}: {preference} ({strength})"
        for food, preference, strength in preferences
    ]
)


# -----------------------------------
# 3. Get today's menu
# -----------------------------------

menu = get_menu(day, meal)

menu_items = [item[0] for item in menu]

menu_text = "\n".join(
    [f"- {item}" for item in menu_items]
)

# -----------------------------------
# 4. Get recent meal history
# -----------------------------------

history = get_recent_history(10)

if history:
    history_text = "\n".join(
        [
            f"- {date}: {food} | {action} | {feedback}"
            for date, food, action, feedback in history
        ]
    )
else:
    history_text = "No recent meal history."


# -----------------------------------
# 4. Connect to Tinker
# -----------------------------------

MODEL_NAME = "Qwen/Qwen3.5-4B"

service_client = tinker.ServiceClient()

sampling_client = service_client.create_sampling_client(
    base_model=MODEL_NAME
)

tokenizer = sampling_client.get_tokenizer()

renderer = renderers.get_renderer(
    "qwen3_5_disable_thinking",
    tokenizer
)


# -----------------------------------
# 5. Build prompt
# -----------------------------------

messages = [
    {
        "role": "system",
        "content": (
            "You are EeshApp, a friendly hostel food companion for Eesha. "
            "Help her decide what to eat from the AVAILABLE MENU.\n\n"

            "IMPORTANT RULES:\n"

            "1. Recommend ONLY foods that appear in the available menu.\n"

            "2. The menu tells you what food is AVAILABLE. It does NOT "
            "tell you what Eesha has already eaten.\n"

            "3. Never claim that Eesha ate, tried, ordered, skipped, or "
            "liked something unless that information is explicitly given "
            "as meal history or feedback.\n"

            "4. Use Eesha's preferences silently to make a better choice. "
            "Do not list all of her likes and dislikes in the response.\n"

           "5. Mention a preference only when it adds real value to the "
"recommendation. It is completely fine to give a recommendation "
"without mentioning any preference.\n"

            "6. Do not mention unavailable foods.\n"

            "7. Do not infer broad preferences. Disliking one food does "
            "not mean Eesha dislikes an entire food category.\n"

            "8. Give a short, natural recommendation for THIS meal.\n"

            "9. Give a genuine reason for the recommendation. The reason "
"can be based on taste, combination, variety, or simple "
"nutritional value when appropriate. Do NOT force a connection "
"to Eesha's stored preferences if that connection is unnecessary.\n"

            "10. You may gently encourage Eesha to try a food she does "
            "not usually prefer if there is a useful reason. For example, "
            "rajma contains plant protein and iron. Do not lecture, guilt, "
            "or give medical advice.\n"

            "11. Do not invent nutritional facts or make exaggerated "
            "health claims.\n"

            "12. Sound like a friend who knows Eesha, not like a nutrition "
            "textbook or a database reading out her profile.\n\n"

            "13. Avoid generic phrases such as 'hits all your favorites', "
"'perfect for your preferences', or 'hits the spot'. Make the "
"recommendation specific to the actual food available today.\n"

"14. Use recent meal history when it is relevant. If Eesha recently "
"disliked a food, take that into account when it appears again. If "
"she recently liked a food, you may consider recommending it again. "
"Do not mention the stored history explicitly unless it feels natural.\n"

            "Most importantly: use the information you have to make the "
            "recommendation smarter, but do not expose or repeat all of "
            "that information unnecessarily."
        )
    },
    {
        "role": "user",
        "content": (
            f"Today is {day}.\n"
            f"Current meal: {meal}.\n\n"

            "Eesha's stored preferences:\n"
            f"{preferences_text}\n\n"

            "AVAILABLE MENU:\n"
            f"{menu_text}\n\n"

            "RECENT MEAL HISTORY:\n"
f"{history_text}\n\n"

            "Recommend what Eesha should eat from today's available menu. "
            "Keep it short, friendly, natural, and specific to this meal."
        )
    }
]


# -----------------------------------
# 6. Generate response
# -----------------------------------

prompt = renderer.build_generation_prompt(messages)

sampling_params = tinker.types.SamplingParams(
    max_tokens=150,
    temperature=0.5
)

result = sampling_client.sample(
    prompt=prompt,
    sampling_params=sampling_params,
    num_samples=1
).result()


# -----------------------------------
# 7. Print response
# -----------------------------------

response = tokenizer.decode(
    result.sequences[0].tokens
)

response = response.replace(
    "<|im_end|>",
    ""
).strip()


print("\n--- EeshApp AI Response ---\n")
print(response)