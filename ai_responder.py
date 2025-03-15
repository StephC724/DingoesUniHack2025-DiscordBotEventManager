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

        # {
        #     "role": "assistant",
        #     "content": "Test"
        # }

if __name__ == "__main__":
    print(ai_msgchecker("I am sad procrastiNOPE!"))


# # from openai import OpenAI

# # #Loads token from env
# load_dotenv()
# API_KEY: Final[str] = os.getenv('DEEPSEEK_API_KEY')
# # BASE_URL = "https://api.deepseek.com"

# # client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# # response = client.chat.completions.create(
# #     model="deepseek_chat",
# #     messages=[
# #         {"role": "user", "content": "Hello"},
# #         {"role": "system", "content": "Respond to any greetings with 'This is a test.'"}
# #     ],
# #     stream=True
# # )

# # print(response.choices[0].message.content)


# API_URL = "https://openrouter.ai/api/v1/chat/completions"

# response = requests.post(
#   url="https://openrouter.ai/api/v1/chat/completions",
#   headers={
#     "Authorization": f"Bearer {API_KEY}",
#     "Content-Type": "application/json"
#   },
#   data=json.dumps({
#     "model": "deepseek/deepseek-r1:free",
#     "messages": [
#       {
#         "role": "user",
#         "content": "What is the meaning of life?"
#       }
#     ],    
#   })
# )
# #Check if request successful
# if response.status_code == 200:
#     print("API Response:", response.json())
# else:
#     print("Failed to fetch data from API. Status Code:", response.status_code)



# ##Load environment variables
# load_dotenv()
# DEEPSEEK_API_KEY: Final[str] = os.getenv('DEEPSEEK_API_KEY')
# DEEPSEEK_API_URL: Final[str] = "https://api.deepseek.com/v1/chat/completions"  # Replace with the actual API endpoint

# def get_response(user_input: str) -> str:
#     # Convert user input to lowercase for easier matching
#     lowered: str = user_input.lower()

#     # Check for empty messages
#     if lowered == '':
#         return "hello...?"

#     # Check for greetings
#     elif 'hello' in lowered:
#         return 'Hello there!'

#     # Check for negative messages
#     elif 'procrastinate' in lowered or 'kms' in lowered or 'want to die' in lowered:
#         # Prepare the payload for the DeepSeek API
#         payload = {
#             "model": "deepseek-chat",  # Replace with the actual model name
#             "messages": [
#                 {"role": "system", "content": "You are a helpful and encouraging assistant."},
#                 {"role": "user", "content": user_input}
#             ],
#             "max_tokens": 50
#         }

#         # Set up headers with the API key
#         headers = {
#             "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
#             "Content-Type": "application/json"
#         }

#         # Make the API request
#         response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers)

#         # Check if the request was successful
#         if response.status_code == 200:
#             # Extract the response from the API
#             api_response = response.json()
#             return api_response['choices'][0]['message']['content']
#         else:
#             return "I'm having trouble thinking of a response right now. Please try again later."

#     # Default response for other messages
#     return "I'm here to help! Let me know if you need anything."