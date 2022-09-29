from inspect import trace
import discord
import os
import logging

from database.database import Guild_DataBase
from classes._logging import _Logging
from dotenv import load_dotenv, find_dotenv
from rich.progress import track
from core.music import * 
from discord.ext import commands, bridge

log = _Logging()
log = logging.getLogger("rich")

#bot = commands.Bot(debug_guilds=["1021249050445611009", "851644348281258035"], intents=discord.Intents.all())
bot = bridge.Bot(debug_guilds=["1021249050445611009", "851644348281258035"], command_prefix="$", intents=discord.Intents.all())

def load_all():
    for filename in track(os.listdir('./core'), description="loading core"):
        if filename.endswith('.py'):
            bot.load_extension(f'core.{filename[:-3]}')

@bot.event
async def on_ready():
    amount = 0
    for count in bot.guilds:
        amount += 1
    log.info(f"Bot is currently in {amount} servers")
    log.info(f"{bot.user} has connected to discord")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="becoming sentient"))

load_all()
load_dotenv(find_dotenv())
bot.run(os.environ.get("TOKEN"))