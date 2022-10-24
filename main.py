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
    await update_notify()

async def update_notify():
    gd = GuildDatabase()
    utils = Utils()
    info = Info(bot)
    version = info.BOT_VERSION
    guild_count = 0
    for c in bot.guilds:
        guild_count += 1
        if gd.get_guild_key(c.id, "update_notify") == "None":
            gd.update_guild_key(c.id, "update_notify", False)
        if gd.get_guild_key(c.id, "update_notify") == "False":
            gd.update_guild_key(c.id, "update_notify", True)
            embed = discord.Embed(title="New Update", description=f"Updated to {version}", color=utils.DEFAULT_COLOR)
            channel_id = db.get_guild_key(c.id, "modlog_channel")
            channel = c.get_channel(int(channel_id))
            await channel.send(embed=embed)
    
async def changelog():
    utils = Utils()
    with open("changelog.txt", "r") as change:
        changeall = change.read()
        
    guild_count = 0
    for c in bot.guilds:
        guild_count += 1
    for c, guild in enumerate(bot.guilds):
        print(guild.id)
        channel_id = db.get_guild_key(guild.id, "modlog_channel")
        channel = guild.get_channel(int(channel_id))
        embed = discord.Embed(title="NEW UPDATE 1.0.0-alpha", description=changeall, color=utils.DEFAULT_COLOR)
        await channel.send(embed=embed)
        print(f"changelog sent to {guild} {c + 1}/{guild_count}")


load_cogs()
load_dotenv(find_dotenv())
bot.run(os.environ.get("TOKEN"))
