# Load the token from the environment variables
from dotenv import load_dotenv
import os
import discord
import random
from ec2_metadata import ec2_metadata

load_dotenv()

# Get the token from the environment variable
token = os.getenv("TOKEN")

# Set up intents for the bot
intents = discord.Intents.default()
intents.message_content = True  # Allows reading message content

# Initialize the bot with intents
client = discord.Client(intents=intents)

# Declare EC2 metadata variables as none, otherwise the program will not run.
# If you set these variables = ec2_metadata.* they will try to pull data that doesn't exist when you run this program outside of EC2.
instanceID = None
instanceRegion = None
instanceIP = None
instanceZone = None
instanceType = None

# Get EC2 metadata and print success message
try:
    instanceID = ec2_metadata.instance_id
    instanceRegion = ec2_metadata.region
    instanceIP = ec2_metadata.public_ipv4
    instanceZone = ec2_metadata.availability_zone
    instanceType = ec2_metadata.instance_type
    print("EC2 Metadata Available")

# If data unavailable, use placeholder data and print failure message
except Exception:
    instanceID = "N/A"
    instanceType = "Python Instance"
    instanceRegion = "N/A"
    instanceIP = "N/A"
    instanceZone = "N/A"
    print("EC2 Metadata Unavailable.")

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    # Get the channel, user, and message content
    username = str(message.author).split("#")[0]
    displayname = str(message.author.display_name).split("#")[0]
    channel = str(message.channel.name)
    servername = str(message.guild.name)
    user_message = str(message.content).lower()
    print(f"Message: \"{user_message}\" by {displayname} on {channel}")

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
        await message.channel.send(f"Hello... {username}, codename '{displayname}'... Say 'Access utility belt' to view my actions 🤖")
        return
    elif user_message in ["bye", "goodbye", "good bye"]:
        await message.channel.send(f"I hope you enjoyed your stay at the {servername}, {displayname}... 🤖")
        return
    # Special utility belt commands
    elif user_message in ["help", "help me", "botsignal"]:
        await message.channel.send(f"Distress call detected, sending help to {displayname}... 🤖")
        await message.channel.send(random.choice(list(utilityBelt.values())))
        return
    elif user_message == "access utility belt":
        await message.channel.send("Here are the items in my utility belt: " + ", ".join(utilityBelt.keys()))
        return
    # Check if the message matches any utility belt item
    elif user_message in utilityBelt:
        await message.channel.send(utilityBelt[user_message])
        return
    
    # Run EC2 diagnostics
    if user_message in ["ec2", "system diagnostics", "run system diagnostics"]:
        await message.channel.send(
            f"Running system diagnostics... 🤖\n"
            f"ID: {instanceID}\n"
            f"Type: {instanceType}\n"
            f"Region: {instanceRegion}\n"
            f"IP: {instanceIP}\n"
            f"Zone: {instanceZone}"
        )
        return
# Run the bot
client.run(token)
