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
from message_track import start_tracking
import discord
from discord import app_commands
from pointSystem import *


#apprently takes like an hour for  commands to be up for the bot on all servers
#this way its just the dev server
MY_GUILD = discord.Object(id=1350063882705829950)

pointSystem = pointSystem()

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        
        



    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


# STEP 0: LOAD OUR TOKEN FROM SOMEWHERE SAFE
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# STEP 1: BOT SETUP, allow bot to access intents
intents: Intents = Intents.default()
intents.message_content = True  # NOQA
client = MyClient(intents=intents)


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

    await check_functions(message)
    await send_message(message, user_message)

    user_id = message.author.id
    if user_id not in message_count:
        message_count[user_id] = 1
    else:
        message_count[user_id] += 1

    # Command-like functionality using messages instead of `@bot.command`
    if message.content.startswith("!start_tracking"):
        try:
            duration = int(message.content.split()[1])  # Get the duration from the message
            await start_tracking(message.channel, duration)
        except (IndexError, ValueError):
            await message.channel.send("Please specify a valid duration for tracking in seconds.")

async def start_tracking(channel, duration):
    message_count.clear()
    
    await channel.send(f"Tracking messages for {duration} seconds...")

    await asyncio.sleep(duration)

    if not message_count:
        await channel.send("No messages were sent during the tracking period.")
    else:
        
        for user,messages in message_count.items():
            pointSystem.userRemovePoints(channel.guild, user, messages)
            
        results = "\n".join([f"<@{user_id}>: {count} messages, " for user_id, count in message_count.items()])
        await channel.send(f"Message count after {duration} seconds:\n{results}")

###
### bot commands
###
@client.tree.command()
#describtion of each value that needs to be input
@app_commands.describe(
    user='the user to give points to',
    amount='The amount of points to give',
)
#sets up command, function name is the name of command    must include interaction
async def giveuserpoints(interaction: discord.Interaction, user: discord.Member, amount: int):
    #command description
    """Give a user points of X amount"""
    ###what ever the command does
    pointSystem.userAddPoints(interaction.guild_id, user, amount)
    ###
    #response
    await interaction.response.send_message(f'gave {amount} points to {user.mention}')

@client.tree.command()
@app_commands.describe(
    user='the user to remove points from',
    amount='The amount of points to remove',
)
async def removeuserpoints(interaction: discord.Interaction, user: discord.Member, amount: int):
    """remove X amount of points from a user"""
    pointSystem.userRemovePoints(interaction.guild_id, user, amount)
    await interaction.response.send_message(f'removed {amount} points from {user.mention}')


@client.tree.command()
@app_commands.describe(
    user='the user you want to see the score of'
)
async def userscore(interaction: discord.Interaction, user: discord.Member):
    """see a users score"""
    #call to retrieve users score
    points = pointSystem.getUserpoints(interaction.guild_id,user)
    await interaction.response.send_message(f'{user.mention} has {points} points')



@client.tree.command()
@app_commands.describe(
)
async def leaderboard(interaction: discord.Interaction):
    """see the top 20 scores on the server"""
    pointSystem.giveLeaderboard(interaction.guild_id)
    await interaction.response.send_message(f'not implemented')

###
###
###



# STEP 5: MAIN ENTRY POINT
def main() -> None:
    client.run(token=TOKEN)


if __name__ == '__main__':
    main()


