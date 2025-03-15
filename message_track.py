from typing import Final
import os
import discord
from discord.ext import commands
from discord import Intents, Client, Message
from responses import get_response
import asyncio
import time

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# STEP 1: BOT SETUP, allow bot to access intents
intents: Intents = Intents.default()
intents.message_content = True  # NOQA
client: Client = Client(intents=intents)

message_count = {}
async def start_tracking(channel, duration):
    message_count.clear()

    await channel.send(f"Tracking messages for {duration} seconds...")

    await asyncio.sleep(duration)

    if not message_count:
        await channel.send("No messages were sent during the tracking period.")
    else:
        results = "\n".join([f"<@{user_id}>: {count} messages" for user_id, count in message_count.items()])
        await channel.send(f"Message count after {duration} seconds:\n{results}")

    
if __name__ == "__main__":
    main()




        

    

    



