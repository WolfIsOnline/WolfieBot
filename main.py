import discord
import os
import rich.progress
from rich.progress import track
from core.music import * 
from discord.ext import commands

bot = commands.Bot(command_prefix=commands.when_mentioned, debug_guilds=["1021249050445611009", "851644348281258035"], intents=discord.Intents.all())

for filename in track(os.listdir('./core'), description="loading core"):
    if filename.endswith('.py'):
        bot.load_extension(f'core.{filename[:-3]}')

async def connect_nodes():
    await bot.wait_until_ready()
    await wavelink.NodePool.create_node(bot=bot, host='0.0.0.0', port=2333, password="youshallnotpass")

invites = {}

@bot.event
async def on_message(message):
    await bot.process_commands(message)

@bot.event
async def on_ready():
    for guild in track(bot.guilds, description="getting guild invites"):
        invites[guild.id] = await guild.invites()
    await connect_nodes()
    print(f"Connected as {bot.user}.")

@bot.event
async def on_wavelink_node_ready(node: wavelink.Node):
    print(f"{node.identifier} is ready.")

with rich.progress.open("token.txt", "r", description="fetching token") as file:
    token = file.read()
file.close()
bot.run(token)