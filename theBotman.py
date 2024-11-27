# Load the token from the environment variables
from dotenv import load_dotenv
import os
import discord
import random
from ec2_metadata import ec2_metadata

load_dotenv()

# Get the token from .env file's variable
token = os.getenv("TOKEN")

# Set up intents for the bot
intents = discord.Intents.default()
intents.message_content = True  # Allows reading message content

# Initialize the bot with intents
client = discord.Client(intents=intents)

# Set EC2 metadata variables as none so code can run.
ec2_ID = None
ec2_Region = None
ec2_IP = None
ec2_Zone = None
ec2_Type = None

# Get EC2 metadata and print success message
try:
    ec2_ID = ec2_metadata.ec2__id
    ec2_Region = ec2_metadata.region
    ec2_IP = ec2_metadata.public_ipv4
    ec2_Zone = ec2_metadata.availability_zone
    ec2_Type = ec2_metadata.ec2__type
    print("EC2 Metadata Available")

# If data unavailable, use placeholder data and print failure message
except Exception:
    ec2_ID = "N/A"
    ec2_Type = "Python ec2_"
    ec2_Region = "N/A"
    ec2_IP = "N/A"
    ec2_Zone = "N/A"
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
            f"ID: {ec2_ID}\n"
            f"Type: {ec2_Type}\n"
            f"Region: {ec2_Region}\n"
            f"IP: {ec2_IP}\n"
            f"Zone: {ec2_Zone}"
        )
        return
# Run the bot
client.run(token)
