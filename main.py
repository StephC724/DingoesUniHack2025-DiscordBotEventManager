from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response
from check_functions import *
#thi stuff
from discord.ext import commands
from discord import Intents, Message
import asyncio
import time
from responses import get_response
import datetime


# STEP 0: LOAD OUR TOKEN FROM SOMEWHERE SAFE
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# STEP 1: BOT SETUP, allow bot to access intents
intents: Intents = Intents.default()
intents.message_content = True  # NOQA
client: Client = Client(intents=intents)

#This stuff

message_count = {}


# STEP 2: MESSAGE FUNCTIONALITY
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message was empty because intents were not enabled)')
        return

    # bot will message user privately if start of user message is '?'
    is_private = user_message[0] == '?'

    if is_private:
        user_message = user_message[1:]

    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


# STEP 3: HANDLING THE STARTUP
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')


# STEP 4: HANDLING INCOMING MESSAGES
@client.event
async def on_message(message: Message) -> None:
    # Don't want bot to talk to itself
    if message.author == client.user:
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')

    #await check_functions(message)
    await send_message(message, user_message)

    user_id = message.author.id
    if user_id not in message_count:
        message_count[user_id] = 1
    else:
        message_count[user_id] += 1

    # Command-like functionality using messages instead of `@bot.command`
    # if message.content.startswith("!start_tracking"):
    #     try:
    #         duration = int(message.content.split()[1])  # Get the duration from the message
    #         await start_tracking(message.channel, duration)
    #     except (IndexError, ValueError):
    #         await message.channel.send("Please specify a valid duration for tracking in seconds.")

async def start_tracking(channel, duration):
    message_count.clear()

    await channel.send(f"Tracking messages for {duration} seconds...")

    await asyncio.sleep(duration)

    if not message_count:
        await channel.send("No messages were sent during the tracking period.")
    else:
        results = "\n".join([f"<@{user_id}>: {count} messages" for user_id, count in message_count.items()])
        await channel.send(f"Message count after {duration} seconds:\n{results}")
    
async def create_event(message: Message):
    """
    Event message format: 
    /em create_event, name, location, start_date, start_time, end_date, end_time

    Creates an event on the Discord server when user sends above formatted message
    """
    message_str = message.content
    name, location, start_d, start_t, end_d, end_t = message_str.split(", ")[1:]
    start_datetime = convert_to_datetime(start_d, start_t)
    end_datetime = convert_to_datetime(end_d, end_t)
    duration = end_datetime - start_datetime
    await discord.Guild.create_scheduled_event(self=message.guild, name=name, location=location, start_time=start_datetime, end_time=end_datetime, entity_type=discord.EntityType.external, privacy_level=discord.PrivacyLevel.guild_only)
    start_tracking(message.channel, duration)

def convert_to_datetime(date, time):
    day, month, year = [int(i) for i in date.split("/")]
    hour, minute = [int(i) for i in time.split(":")]
    dt = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute)
    dt = dt.replace(tzinfo=datetime.timezone.utc)
    return dt


async def get_events(server):
    return await discord.Guild.fetch_scheduled_events(guild=server)



# STEP 5: MAIN ENTRY POINT
def main() -> None:
    client.run(token=TOKEN)


if __name__ == '__main__':
    main()
