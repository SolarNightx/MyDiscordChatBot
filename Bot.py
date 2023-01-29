# bot.py
import os
import discord
import json
import random
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from dotenv import load_dotenv

# adding language for compatibility with spacy 3.0
class ENGSM:
    ISO_639_1 = 'en_core_web_sm'

chatbot = ChatBot(
    "Ryan",
    tagger_language=ENGSM     # <-- pass this new language here
)
trainer = ListTrainer(chatbot)

random.seed()

with open("data.json", "r") as read_file:
    data = json.load(read_file)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents().default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):
    print(f'{message.author} in {message.channel}: {message.content}')

    if message.author == client.user:
        return
        
    if message.content == '99!':
        response = 'I\'m the human form of the 💯 emoji.'
        await message.channel.send(response)

    if message.channel.id == 984410953271615548:
        response = chatbot.get_response(message.content)
        await message.channel.send(response)
    elif random.randint(1,10) == 5:
        response = chatbot.get_response(message.content)
        await message.channel.send(response)

for i in data['conversations']:
    trainer.train(i)

client.run(TOKEN)