import discord
import os

from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TOKEN")
if not token:
    raise ValueError("ERROR: Bot token is missing. Check your .env file.")



intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents = intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$fc'):
        await message.channel.send('Fact Checking..')

client.run(token)

