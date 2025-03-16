from groq import Groq

client = Groq()
completion = client.chat.completions.create(
    model="llama3-70b-8192",
    messages=[
        {
            "role": "user",
            "content": "Distinguish negative messages relating to procrastination or depression from positive study and learning related messages. If the message is something like \"I want to procrastinate\" or \"this assignment makes me want to KMS\", you should reply with a message of encouragement like \"you can do it!\" "
        },
        {
            "role": "assistant",
            "content": "I'd be happy to help distinguish between negative and positive messages and respond accordingly. Here are some examples:\n\n**Negative Messages:**\n\n* \"I want to procrastinate\" -> \"You can do it! Break down the task into smaller chunks and focus on one step at a time. You got this!\"\n* \"This assignment makes me want to KMS\" -> \"I know it's tough, but you're capable of getting through it. Take a deep breath, grab a snack or a drink, and let's tackle it together!\"\n* \"I'll never be able to finish this\" -> \"Don't give up! You've made it this far, and you can keep going. What's the next step you need to take to move forward?\"\n* \"I'm so depressed, I don't want to do anything\" -> \"I'm here for you, and I care. It's okay to feel overwhelmed, but don't let it stop you from taking small steps towards your goals. What's one tiny thing you can do today to move forward?\"\n\n**Positive Messages:**\n\n* \"I'm so excited to start this project!\" -> \"That's great to hear! What's your plan of attack? Do you have all the resources you need to get started?\"\n* \"I just learned something new and it's amazing!\" -> \"That's awesome! What did you learn? Can you tell me more about it?\"\n* \"I'm on a roll with my studying!\" -> \"Keep that momentum going! You're doing great. What's your strategy for staying focused and motivated?\"\n* \"I finally understand this concept!\" -> \"Congratulations! That's a huge accomplishment. How did you manage to grasp it? Can you explain it to me?\"\n\nRemember, my goal is to provide encouragement and support while helping you stay focused on your goals. If you're feeling overwhelmed or struggling with negative thoughts, I'm here to listen and offer guidance."
        }
    ],
    temperature=1,
    max_completion_tokens=1024,
    top_p=1,
    stream=True,
    stop=None,
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")
