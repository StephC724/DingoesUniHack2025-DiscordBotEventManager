from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from check_functions import *
from event_management import create_event

async def check_functions(message: Message):
    message_str = message.content
    if "create_event" in message_str:
        print("Trying to trigger message")
        await create_event(message)