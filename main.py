from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from check_functions import *
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
pointSystem = pointSystem()



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

    await check_functions(message)
    # await send_encouraging_msg(message, user_message)

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
            print(f"Removing {messages} points from user {user}.")
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
    points = pointSystem.getUserPoints(interaction.guild_id,user)
    await interaction.response.send_message(f'{user.mention} has {points} points')



@client.tree.command()
@app_commands.describe(
)
async def leaderboard(interaction: discord.Interaction):
    """see the top 20 scores on the server"""
    temp_leaderboard = pointSystem.giveLeaderboard(interaction.guild_id)
    leaderboard = []
    for user in temp_leaderboard:
        leaderboard.append(MemberConverter().convert(ctx, user)
)  
    await interaction.response.send_message(f'{leaderboard}')


###
###
###



#MAIN ENTRY POINT (turns on bot)
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()
