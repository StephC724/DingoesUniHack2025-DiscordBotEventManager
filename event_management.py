from main import main
from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
import discord
from datetime import *
import pytz

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
    await discord.Guild.create_scheduled_event(self=message.guild, name=name, location=location, start_time=start_datetime, end_time=end_datetime, entity_type=discord.EntityType.external, privacy_level=discord.PrivacyLevel.guild_only)


def convert_to_datetime(date:str, time:str):
    day, month, year = [int(i) for i in date.split("/")]
    hour, minute = [int(i) for i in time.split(":")]
    tz = pytz.timezone('Australia/Sydney')
    dt = datetime(year=year, month=month, day=day, hour=hour, minute=minute)
    dt = tz.localize(dt)
    return dt


async def get_events(server:discord.Guild):
    return await server.fetch_scheduled_events()


async def get_current_events(server:discord.Guild):
    all_events = await get_events(server)
    now = datetime.now(timezone.utc)
    current_events = []
    for event in all_events:
        if is_current_event(event, now):
            current_events.append(event)
    return current_events


def is_current_event(event:discord.ScheduledEvent, now:datetime):
    if event.start_time <= now <= event.end_time:
        return True
    else:
        return False