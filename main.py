from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from event_management import *
#thi stuff
from discord.ext import commands
from discord import Intents, Message
import asyncio
import time
import datetime
from message_track import start_tracking
import discord
from discord import app_commands
from pointSystem import *
from discord.ext.commands import MemberConverter
from ai_responder import ai_msgchecker, ai_response

#apprently takes like an hour for  commands to be up for the bot on all servers
#this way its just the dev server
MY_GUILD = discord.Object(id=1350063882705829950)
pointSystemObj = pointSystem()
tracking = False


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        
        


    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)




#Loads Discord API token from virtual environment
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')


#Bot Setup -> Allows bot to access intents
intents: Intents = Intents.default()
intents.message_content = True  # NOQA
client = MyClient(intents=intents)


#This stuff

message_count = {}

#AI-Generated Encouragement Message Function
async def send_encouraging_msg(message:Message, user_message:str) -> None:
    if not user_message:
        print('(Message was empty because intents were not enabled)')
        return
    try:
        require_response = ai_msgchecker(user_message)
        if require_response == "True":
            response = ai_response(user_message)
            #Sends encouraging message in channel the user msg was sent in
            await message.channel.send(response)
    except Exception as e:
        print(e)

#Handles Start-Up
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')

#Handles incoming messages
@client.event
async def on_message(message: Message) -> None:
    #Prevents bot from talking to itself
    if message.author == client.user:
        return

    #DEBUGGING
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)
    print(f'[{channel}] {username}: "{user_message}"')

    # await send_encouraging_msg(message, user_message)

    user_id = message.author.id
    if user_id not in message_count:
        message_count[user_id] = 1
    else:
        message_count[user_id] += 1

    current_events = await get_current_events(message.guild)
    if len(current_events) > 0: #Is the message sent during a study session
        print("Attempted to deduct points")
        pointSystemObj.userRemovePoints(message.guild.id, message.author, 1)

    if tracking: #If tracking the amount of messages in a time period
        print("Points attempted to remove")
        pointSystemObj.userRemovePoints(serverID=message.guild.id, userID=message.author, points_amount=1)

    # Command-like functionality using messages instead of `@bot.command`
    if message.content.startswith("!start_tracking"):
        try:
            duration = int(message.content.split()[1])  # Get the duration from the message
            await start_tracking(message.channel, duration)
        except (IndexError, ValueError):
            await message.channel.send("Please specify a valid duration for tracking in seconds.")

async def start_tracking(channel, duration):
    tracking = True
    message_count.clear()
    
    await channel.send(f"Tracking messages for {duration} seconds...")

    await asyncio.sleep(duration)

    tracking = False

    if not message_count:
        await channel.send("No messages were sent during the tracking period.")
    else:
        
        # for user,messages in message_count.items():
        #     print(f"Removing {messages} points from user {user}.")
        #     pointSystemObj.userRemovePoints(channel.guild, user, messages)
            
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
    pointSystemObj.userAddPoints(interaction.guild_id, user.id, amount)
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
    pointSystemObj.userRemovePoints(interaction.guild_id, user.id, amount)
    await interaction.response.send_message(f'removed {amount} points from {user.mention}')


@client.tree.command()
@app_commands.describe(
    user='the user you want to see the score of'
)
async def userscore(interaction: discord.Interaction, user: discord.Member):
    """see a users score"""
    
    #call to retrieve users score
    points = pointSystemObj.getUserPoints(interaction.guild_id,user.id)
    await interaction.response.send_message(f'{user.mention} has {points} points')



@client.tree.command()
@app_commands.describe(
)
async def leaderboard(interaction: discord.Interaction):
    """see the top 20 scores on the server"""
    temp_leaderboard = pointSystemObj.giveLeaderboard(interaction.guild_id)
    leaderboard = []
    for user in temp_leaderboard:
        member = user
        #interaction.guild.get_member(int(user))
        leaderboard.append(f'{member} score: {temp_leaderboard[user]['UserPoints']} \n'
)  
    response = f"LeaderBoard for {interaction.guild} \n"
    for line in leaderboard:
        response = (response + "" + line)
    await interaction.response.send_message(response)

@client.tree.command()
#describtion of each value that needs to be input
@app_commands.describe(
    name='The name of the event',
    location='The amount of points to give',
    start_date='The start date of the event in DD/MM/YYYY',
    start_time='The start time of the event in 24 hour AEST HH:MM',
    end_date='The start date of the event in DD/MM/YYYY',
    end_time='The end time of the event in 24 hour AEST HH:MM'
)
async def create_event(interaction: discord.Interaction, name:str, location:str, start_date:str, start_time:str, end_date:str, end_time:str):
    """
    Event message format: 
    /em create_event, name, location, start_date, start_time, end_date, end_time

    Creates an event on the Discord server when user sends above formatted message
    """
    start_datetime = convert_to_datetime(start_date, start_time)
    end_datetime = convert_to_datetime(end_date, end_time)
    await discord.Guild.create_scheduled_event(self=interaction.guild, name=name, location=location, start_time=start_datetime, end_time=end_datetime, entity_type=discord.EntityType.external, privacy_level=discord.PrivacyLevel.guild_only)
    await interaction.response.send_message(f'{name} has been created, double check events')

###
###
###



#MAIN ENTRY POINT (turns on bot)
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()
