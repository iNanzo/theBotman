# Load the token from the environment variables
from dotenv import load_dotenv
import os
import discord
import random

load_dotenv()

# Get the token from the environment variable
token = os.getenv("TOKEN")

# Set up intents for the bot
intents = discord.Intents.default()
intents.message_content = True  # Allows reading message content

# Initialize the bot with intents
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    # Get the channel, user, and message content
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    servername = str(message.guild.name)
    user_message = str(message.content).lower()
    print(f"Message: \"{user_message}\" by {username} on {channel}")

    if message.author == client.user:
        return

    # Utility belt items and their responses
    utilityBelt = {
        "botorang": "Sending out Botorang... *WOOSH* 🌀",
        "botmobile": "Starting Botmobile engines... *VROOM VROOM* 🚗💨",
        "botsuit": "Botsuit primed and ready... *BEEP BOOP* 🤖🦸",
        "bothook": "Deploying Bothook!... *SWOOSH, CLANK!* :knot::hook:"
    }

    # Hello/Bye Respond based on message content
    if user_message in ["hello", "hi"]:
        await message.channel.send(f"Hello... {username}... Say 'Access utility belt' to view my actions 🤖")
        return
    elif user_message == "bye":
        await message.channel.send(f"I hope you enjoyed your stay at the {servername}, {username}... 🤖")
        return
    elif user_message in ["help", "help me", "botsignal"]:
        await message.channel.send(f"Distress call detected, sending help to {username}... 🤖")
        await message.channel.send(random.choice(list(utilityBelt.values())))
        return
    elif user_message == "access utility belt":
        await message.channel.send("Here are the items in my utility belt: " + ", ".join(utilityBelt.keys()))
        return

    # Check if the message matches any utility belt item
    if user_message in utilityBelt:
        await message.channel.send(utilityBelt[user_message])
        return

# Run the bot
client.run(token)
