from inspect import trace
import discord
import os

from dotenv import load_dotenv, find_dotenv
from rich.progress import track
from core.music import *
from discord.ext import bridge
from discord.ext.bridge import BridgeContext
from database.database import GuildDatabase
from core.info import Info


bot = bridge.Bot(command_prefix=".", debug_guilds=["1021249050445611009"], intents=discord.Intents.all())


db = GuildDatabase()
def load_all():
    for filename in track(os.listdir('./core'), description="loading core"):
        if filename.endswith('.py'):
            bot.load_extension(f'core.{filename[:-3]}')


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


load_all()
load_dotenv(find_dotenv())
bot.run(os.environ.get("TOKEN"))
