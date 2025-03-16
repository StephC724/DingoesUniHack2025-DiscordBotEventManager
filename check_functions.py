from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from check_functions import *
from event_management import *
from pointSystem import *

async def check_functions(message: Message):
    message_str = message.content
    if "create_event" in message_str:
        await create_event(message)

    current_events = await get_current_events(message.guild)
    print(current_events)
    if len(current_events) > 0: #Is the message sent during a study session
        print("Message sent during study session")
        pointSystem.userRemovePoints(message.guild, message.author, 1)