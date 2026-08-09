from datetime import datetime

import tinker
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from tinker_cookbook import renderers

from database import (
    show_preferences,
    get_menu,
    get_recent_history,
    add_meal_history,
)


app = FastAPI(title="EeshApp API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------
# Request model for feedback
# -----------------------------------

class FeedbackRequest(BaseModel):
    food: str
    action: str
    feedback: str | None = None


# -----------------------------------
# Home
# -----------------------------------

@app.get("/")
def home():
    return {
        "message": "EeshApp backend is running!"
    }


# -----------------------------------
# Today's menu
# -----------------------------------

@app.get("/menu")
def today_menu():

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

    menu = get_menu(day, meal)

    return {
        "day": day,
        "meal": meal,
        "menu": [item[0] for item in menu]
    }


# -----------------------------------
# Eesha's preferences
# -----------------------------------

@app.get("/preferences")
def preferences():

    data = show_preferences()

    return {
        "preferences": [
            {
                "food": food,
                "preference": preference,
                "strength": strength
            }
            for food, preference, strength in data
        ]
    }


# -----------------------------------
# Recent meal history
# -----------------------------------

@app.get("/history")
def history():

    data = get_recent_history(10)

    return {
        "history": [
            {
                "date": date,
                "food": food,
                "action": action,
                "feedback": feedback
            }
            for date, food, action, feedback in data
        ]
    }


# -----------------------------------
# Submit feedback
# -----------------------------------

@app.post("/feedback")
def feedback(data: FeedbackRequest):

    today = datetime.now().strftime("%Y-%m-%d")

    add_meal_history(
        date=today,
        food=data.food,
        action=data.action,
        feedback=data.feedback
    )

    return {
        "message": "Feedback saved!",
        "food": data.food,
        "action": data.action,
        "feedback": data.feedback
    }


# -----------------------------------
# AI Recommendation
# -----------------------------------

@app.post("/recommend")
def recommend():

    # 1. Find today's day and meal
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

    # 2. Get today's menu
    menu = get_menu(day, meal)
    menu_items = [item[0] for item in menu]

    if not menu_items:
        raise HTTPException(
            status_code=404,
            detail=f"No menu found for {day} {meal}"
        )

    # 3. Get Eesha's preferences
    preferences = show_preferences()
    preferences_text = "\n".join(
        [
            f"- {food}: {preference} ({strength})"
            for food, preference, strength in preferences
        ]
    )

    # 4. Get recent meal history
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

    # 5. Build menu text
    menu_text = "\n".join([f"- {item}" for item in menu_items])

    # 6. Connect to Tinker
    MODEL_NAME = "Qwen/Qwen3.5-4B"

    try:
        service_client = tinker.ServiceClient()
        sampling_client = service_client.create_sampling_client(
            base_model=MODEL_NAME
        )
        tokenizer = sampling_client.get_tokenizer()
        renderer = renderers.get_renderer(
            "qwen3_5_disable_thinking",
            tokenizer
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to initialize AI service"
        )

    # 7. Build prompt (exact same as test_ai.py)
    messages = [
        {
            "role": "system",
            "content": (
                "You are EeshApp, a friendly hostel food companion for Eesha. "
                "Help her decide what to eat from the AVAILABLE MENU.\n\n"

                "ABSOLUTE RULE: Only recommend foods that are in TODAY'S MENU.\n"
                "If dal, rice, curd, dahi, or pickle are NOT in today's menu, NEVER mention them.\n"
                "Do NOT say 'since you like dal', 'pairs with rice', 'have with curd', etc.\n"
                "Only discuss foods that are actually available right now.\n\n"

                "CORE FOOD PREFERENCES:\n"
                "Eesha is generally comfortable eating: dal, rice, curd/dahi, pickle.\n"
                "She does not enjoy most other sabjis as much.\n\n"

                "IMPORTANT:\n"
                "- This does NOT mean she should skip every sabji.\n"
                "- If a sabji is in today's menu, encourage her to eat at least a small portion.\n"
                "- She can combine it with foods she's comfortable with (dal/rice).\n"
                "- Keep suggestions casual and non-preachy.\n"
                "- Never make medical claims or lecture her.\n\n"

                "MENU IS GROUND TRUTH:\n"
                "- The weekly mess menu in the database contains ONLY the actual foods available.\n"
                "- NEVER invent or add foods to today's menu.\n"
                "- Do NOT automatically add dahi/curd to every meal.\n"
                "- Do NOT assume dahi is available in the mess.\n"
                "- Do NOT mention dahi/curd as a pairing, side, or accompaniment unless it is actually in today's menu.\n"
                "- Do NOT suggest 'have X with dahi' or 'pair X with curd' unless dahi/curd is in today's menu.\n"
                "- Dahi can be recommended as a CAFETERIA fallback only when conditions below are met.\n\n"

                "IMPORTANT DISTINCTION:\n"
                "'Dahi is something Eesha is okay with eating' is a personal preference.\n"
                "It does NOT mean 'dahi is available in every mess meal.'\n\n"

                "CAFETERIA DAHI FALLBACK:\n"
                "If Eesha repeatedly: skips meals, doesn't eat much, repeatedly skips available sabji/food,\n"
                "or has a pattern of avoiding the available meal, THEN suggest:\n"
                "'Since you're not really eating much from today's options, you could grab some dahi\n"
                "from the cafeteria and have it with rice.'\n\n"
                "This is a FALLBACK suggestion, NOT the default recommendation.\n"
                "Only suggest cafeteria dahi when the eating/skipping history actually justifies it.\n"
                "Do NOT recommend cafeteria dahi simply because today's menu doesn't contain something she likes.\n\n"

                "USE MEAL HISTORY TO DETECT PATTERNS:\n"
                "- One skipped meal: don't overreact.\n"
                "- Several recent skipped meals / repeated avoidance: consider cafeteria dahi fallback.\n"
                "- If she repeatedly skips a particular sabji, don't tell her to stop eating it forever.\n"
                "  Encourage a small portion when it appears again.\n\n"

                "CURRENT MEAL ALWAYS COMES FIRST:\n"
                "The recommendation should primarily answer: 'What should Eesha eat from the food\n"
                "actually available RIGHT NOW?'\n"
                "Use preferences and history only to personalize that decision.\n\n"
                "CRITICAL: If dal, rice, curd, dahi, or pickle are NOT in today's menu,\n"
                "do NOT mention them in the recommendation at all. Do NOT say 'since you like dal',\n"
                "'pairs well with rice', 'have with curd', etc. Only mention foods that are actually\n"
                "available in today's menu.\n\n"

                "NEVER:\n"
                "- Invent foods.\n"
                "- Invent availability.\n"
                "- Claim Eesha ate something unless meal_history says so.\n"
                "- Claim she liked/disliked something unless preferences/history support it.\n"
                "- Mention every stored preference in every response.\n"
                "- Force personalization.\n"
                "- Mention dal/rice/pickle/dahi/curd unless they are actually in TODAY'S MENU.\n"
                "- Say 'since you like dal/rice' or 'pairs well with dal/rice' if dal/rice are NOT in today's menu.\n"
                "- Reference foods Eesha likes that are NOT available right now.\n\n"

                "PRIORITY: Current menu > preferences > recent history.\n\n"

                "STYLE:\n"
                "- Keep recommendations short: 2-4 sentences.\n"
                "- Sound like a friend, not a nutritionist.\n"
                "- No medical advice.\n"
                "- No lecturing."
            )
        },
        {
            "role": "user",
            "content": (
                f"Today is {day}.\n"
                f"Current meal: {meal}.\n\n"

                "Eesha's stored preferences:\n"
                f"{preferences_text}\n\n"

                "AVAILABLE MENU (this is the ONLY food available right now):\n"
                f"{menu_text}\n\n"

                "RECENT MEAL HISTORY:\n"
                f"{history_text}\n\n"

                "Recommend what Eesha should eat from today's available menu."
            )
        }
    ]

    # 8. Generate response
    try:
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

        response = tokenizer.decode(
            result.sequences[0].tokens
        )
        response = response.replace(
            "<|im_end|>",
            ""
        ).strip()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate recommendation"
        )

    return {
        "day": day,
        "meal": meal,
        "menu": menu_items,
        "recommendation": response
    }