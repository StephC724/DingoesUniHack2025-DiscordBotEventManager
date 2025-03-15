from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from check_functions import *

from ai_responder import ai_msgchecker, ai_response

#Loads Discord API token from virtual environment
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

#Bot Setup -> Allows bot to access intents
intents: Intents = Intents.default()
intents.message_content = True  # NOQA
client: Client = Client(intents=intents)

#AI-Generated Encouragement Message Function
async def send_encouraging_msg(message:Message, user_message:str) -> None:
    if not user_message:
        print('(Message was empty because intents were not enabled)')
        return
    try:
        require_response = ai_msgchecker(user_message)
        if require_response == "True":
            response = ai_response(user_message)
        else:
            response = require_response
        #Sends encouraging message in channel the user msg was sent in
        await message.channel.send(response)
    except Exception as e:
        print(e)

#Handles Startup
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')

#Handles incoming messages
@client.event
async def on_message(message: Message) -> None:
    # Don't want bot to talk to itself
    if message.author == client.user:
        return

    #DEBUGGING
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)
    print(f'[{channel}] {username}: "{user_message}"')

    await check_functions(message)
    await send_encouraging_msg(message, user_message)




# STEP 5: MAIN ENTRY POINT
def main() -> None:
    client.run(token=TOKEN)


if __name__ == '__main__':
    main()




# async def send_message(message: Message, user_message: str) -> None:
#     if not user_message:
#         print('(Message was empty because intents were not enabled)')
#         return

#     # # bot will message user privately if start of user message is '?'
#     # is_private = user_message[0] == '?'
#     # if is_private:
#     #     user_message = user_message[1:]

#     try:
#         # response: str = get_response(user_message) Hard-coded response
#         #We want AI response, so we'll call the AI here
#         await message.author.send(response) if is_private else await message.channel.send(response)
#             #Sends response message
#     except Exception as e:
#         print(e)

# async def send_encouragement_msg(message:Message, user_message:str) -> None:
#     if not user_message:
#         print('(Message was empty because intents were not enabled)')
#         return

#     try:
#         response = genai_response()
#         #Sends message in channel
#         await message.channel.send(response)
#     except Exception as e:
#         print(e)