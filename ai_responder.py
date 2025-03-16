import os
from dotenv import load_dotenv
from groq import Groq

def ai_msgchecker(user_message:str) -> str:
    #Loads API key from virtual environment
    load_dotenv()
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')

    #Runs API
    client = Groq(api_key=GROQ_API_KEY)

    #Screen the user message
    chat_completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "user",
                "content": f"Read this message: {user_message}. If the message is related to procrastination or if the message indicates negativity or sad emotions or if it mentions the name 'procrastiNOPE', return True. Otherwise return False. Limit response to one word."
            }
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )
    return chat_completion.choices[0].message.content

def ai_response(user_message:str) -> str:
    #Loads API key from virtual environment
    load_dotenv()
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')

    #Runs API
    client = Groq(api_key=GROQ_API_KEY)

    #Generates GenAI response to user message and then returns it
    chat_completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "user",
                "content": f"Read this message: {user_message}. You are a Discord bot named 'procrastiNOPE'. Only do the following if the message is related to procrastination or despondency. Respond to any other unrelated messages with 'Test'. , whose goal is to encourage students to not give up on studying and uplift them. Don't say anything that makes you send like a GenAI. Limit it to two sentences."
            }
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )
    return chat_completion.choices[0].message.content

if __name__ == "__main__":
    print(ai_msgchecker("I am sad procrastiNOPE!"))