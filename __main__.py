import hikari
import lightbulb
import os
import logging
import uvloop

from pathlib import Path
from hikari.events.base_events import EventT
from lightbulb.errors import ExtensionNotFound
from wolfiebot.database.database import Database
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
DISCORD_API_KEY = os.environ.get("DISCORD_API_KEY")

log = logging.getLogger(__name__)
bot = lightbulb.BotApp(token=DISCORD_API_KEY, prefix="!", intents=hikari.Intents.ALL, default_enabled_guilds=[], help_class=None, logs="INFO")
database = Database()

@bot.listen(hikari.StartedEvent)
async def start(event) -> None:
    await bot.update_presence(status=hikari.Status.ONLINE, activity=hikari.Activity(name=database.read_user_data(bot.get_me().id, "status"), type=hikari.ActivityType.PLAYING,),)

core = ["quotes", "rooms", "logs", "welcome", "autorole"]
for c in core:
    bot.load_extensions(f"wolfiebot.core.{c}")

commands = ["user", "dev", "admin", "economy", "owner"]
for c in commands:
    bot.load_extensions(f"wolfiebot.commands.{c}")

games = ["slots", "casino"]
for c in games:
    bot.load_extensions(f"wolfiebot.games.{c}")

ai = ["chat", "voice"]
for c in ai:
    bot.load_extensions(f"wolfiebot.ai.{c}")

@bot.listen(hikari.ExceptionEvent)
async def on_error(event: hikari.ExceptionEvent[EventT]) -> None:
    raise event.exception

@bot.listen(lightbulb.CommandErrorEvent)
async def on_command_error(event: lightbulb.CommandErrorEvent) -> None:
    exc = event.exception

    if isinstance(exc, lightbulb.NotOwner):
        await event.context.respond("You do not have access to this command")

    if isinstance(exc, lightbulb.CommandIsOnCooldown):
        seconds = exc.retry_after
        time = await format_time(seconds)
        await event.context.respond(f"Command is on cooldown, retry in {time}")

async def format_time(seconds):
    minutes = int(seconds // 60)
    hours = int(minutes // 60)
    days = int(hours // 24)
    years = int(days // 365)

    time_units = [
        (years, 'year'),
        (days % 365, 'day'),
        (hours % 24, 'hour'),
        (minutes % 60, 'minute'),
        (int(seconds) % 60, 'second')
    ]

    result = []
    for value, unit in time_units:
        if value != 0:
            result.append(f"{value} {unit if value == 1 else unit+'s'}")

    return ', '.join(result)

if __name__ == "__main__":
    uvloop.install()
    bot.run()
