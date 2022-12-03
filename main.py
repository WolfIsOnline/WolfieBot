from inspect import trace
import discord
import os

from dotenv import load_dotenv, find_dotenv
from discord.ext import commands
from rich.progress import track
from discord.ext import bridge
from discord.ext.bridge import BridgeContext
from database.database import GuildDatabase
from cogs.info import Info
from classes.utils import Utils


bot = bridge.Bot(command_prefix=".", intents=discord.Intents.all(), help_command=None)


db = GuildDatabase()
def load_cogs():
    cogs = [
        "cogs.admincommands",
        "cogs.automove",
        "cogs.autorole",
        "cogs.dev",
        "cogs.economy",
        "cogs.usercommands",
        "cogs.info",
        "cogs.modlogs",
        "cogs.music",
        "cogs.nocturnia",
        "cogs.ownercommands",
        "cogs.patches",
        "cogs.polls",
        "cogs.quotes",
        "cogs.simpleembed",
        "cogs.welcome",
        "cogs.crime.heist"
    ]
    for c in cogs:
        bot.load_extension(c)
        print(f"{c} extension loaded")


@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond(error)
    elif isinstance(error, commands.NotOwner):
        await ctx.respond(error)
    else:
        raise error


@bot.event
async def on_ready():
    guilds = 0
    for c in bot.guilds:
        guilds += 1
    print(f"Bot is currently in {guilds} servers")
    print(f"{bot.user} has connected to discord")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="becoming sentient"))

load_cogs()
load_dotenv(find_dotenv())
bot.run(os.environ.get("TOKEN"))
