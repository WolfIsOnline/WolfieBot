from inspect import trace
import discord
import os
import logging

from database.guild_db import Guild_DataBase
from classes._logging import _Logging
from dotenv import load_dotenv, find_dotenv
from rich.progress import track
from core.music import * 
from discord.ext import commands

load_dotenv(find_dotenv())
TOKEN = os.environ.get("TOKEN")

_Logging()
log = logging.getLogger("rich")

bot = commands.Bot(command_prefix=commands.when_mentioned, debug_guilds=["1021249050445611009", "851644348281258035"], intents=discord.Intents.all())
for filename in track(os.listdir('./core'), description="loading core"):
    if filename.endswith('.py'):
        bot.load_extension(f'core.{filename[:-3]}')

async def connect_nodes():
    await bot.wait_until_ready()
    await wavelink.NodePool.create_node(bot=bot, host='0.0.0.0', port=2333, password="youshallnotpass")

@bot.event
async def on_guild_join(guild):
    db = Guild_DataBase()
    db.add_guild(guild.id)


@bot.event
async def on_ready():
    await connect_nodes()
    amount = 0
    for count in bot.guilds:
        amount += 1
    log.info(f"Bot is currently in {amount} servers")
    log.info(f"{bot.user} has connected to discord")

@bot.event
async def on_wavelink_node_ready(node: wavelink.Node):
    log.info(f"node {node.identifier} is ready on port {node._port}")

bot.run(TOKEN)