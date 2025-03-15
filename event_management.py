from main import main
from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
import discord
from responses import get_response
import datetime

async def create_event(message: Message):
    """
    Event message format: 
    /em create_event, name, location, start_date, start_time, end_date, end_time
    """
    message_str = message.content
    name, location, start_d, start_t, end_d, end_t = message_str.split(", ")[1:]
    start_datetime = convert_to_datetime(start_d, start_t)
    end_datetime = convert_to_datetime(end_d, end_t)
    await discord.Guild.create_scheduled_event(self=message.guild, name=name, location=location, start_time=start_datetime, end_time=end_datetime, entity_type=discord.EntityType.external, privacy_level=discord.PrivacyLevel.guild_only)


def convert_to_datetime(date, time):
    day, month, year = [int(i) for i in date.split("/")]
    hour, minute = [int(i) for i in time.split(":")]
    dt = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute)
    dt = dt.replace(tzinfo=datetime.timezone.utc)
    return dt


if __name__ == "__main__":
    main()
    