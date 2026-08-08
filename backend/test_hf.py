from huggingface_hub import InferenceClient

client = InferenceClient()

response = client.chat.completions.create(
    model="meta-llama/Llama-3.2-3B-Instruct",
    messages=[
        {
            "role": "system",
            "content": (
                "You are EeshApp, a friendly hostel food companion. "
                "Give short, practical and personalized suggestions. "
                "Do not give medical advice."
            ),
        },
        {
            "role": "user",
            "content": (
                "Eesha dislikes gatte ki sabji. "
                "She likes dal, rice and curd. "
                "Today's mess menu is gatte ki sabji, dal, rice, curd and roti. "
                "What should Eesha eat today?"
            ),
        },
    ],
    max_tokens=150,
    temperature=0.7,
)

print("\n--- EeshApp AI Response ---\n")
print(response.choices[0].message.content)