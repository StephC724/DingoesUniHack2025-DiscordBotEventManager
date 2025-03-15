from typing import Final
import os
import discord
from discord import Intents, Client, Message, commands
from responses import get_response
import asyncio
import time

intents = discord.Intents.default()
intents.message_content = True  # Enable access to message content
bot = commands.Bot(command_prefix='em/',intents = intents)
message_count = {}

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    user_id = message.author.id
    if user_id not in message_count:
        message_count[user_id] = 1
    else:
        message_count[user_id] += 1

    await bot.process_commands(message)

@bot.commands(name="start_tracking")
async def start_tracker(duration, ctx):
    await ctx.send('start_tracking')
    
    message_count.clear()

    await asyncio.sleep(duration)

    if not message_count:
        await ctx.send("No messages were sent during the tracking period.")
    else:
        results = "\n".join([f"<@{user_id}>: {count} messages" for user_id, count in message_count.items()])
        await ctx.send(f"Message count after {duration} seconds:\n{results}")

    





        

    

    



