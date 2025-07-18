import disnake
import json
import os 
from disnake.ext import commands
from db.db import Database
from dotenv import load_dotenv
from config import config

db = Database("db/db.db")
load_dotenv()

bot = commands.Bot(command_prefix=None, intents=disnake.Intents.all(), sync_commands = True)

@bot.event
async def on_ready():
    await bot.change_presence(status = disnake.Status.online)
    
    await db.init_db()

    print(f'Bot - {bot.user}')
    print(f'API Version - disnake-{disnake.__version__}')
    print("========================")

for filename in os.listdir('./manage'):
    if filename.endswith('.py'):
        bot.load_extension(f'manage.{filename[:-3]}')
        print(f'Manage - {filename}')

for filename in os.listdir('./events/antiraid'):
    if filename.endswith('.py'):
        bot.load_extension(f'events.antiraid.{filename[:-3]}')
        print(f'Antiraid Event - {filename}')

for filename in os.listdir('./events/antinuke'):
    if filename.endswith('.py'):
        bot.load_extension(f'events.antinuke.{filename[:-3]}')
        print(f'Antinuke Event - {filename}')

bot.run(config['token'])
