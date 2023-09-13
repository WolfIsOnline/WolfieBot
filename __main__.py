"""
Entrance
"""

import os
import logging
import hikari
import lightbulb
import uvloop

from hikari.events.base_events import EventT
from dotenv import load_dotenv, find_dotenv
# pylint: disable=no-name-in-module, import-error
from wolfiebot.database.database import Database

load_dotenv(find_dotenv())
DISCORD_API_KEY = os.environ.get("DISCORD_API_KEY")

log = logging.getLogger(__name__)
bot = lightbulb.BotApp(
    token=DISCORD_API_KEY,
    prefix="!",
    intents=hikari.Intents.ALL,
    default_enabled_guilds=[],
    help_class=None,
    logs="INFO"
)
database = Database()

@bot.listen(hikari.StartedEvent)
async def start(event) -> None:
    """
    Event listener for the bot startup.

    Args:
        event: The event object representing the bot startup event.

    Returns:
        None
    """
    await bot.update_presence(
        status=hikari.Status.ONLINE,
        activity=hikari.Activity(name=database.read_user_data(bot.get_me().id, "status"),
                                 type=hikari.ActivityType.PLAYING,
                            ),
        )

core = ["quotes", "rooms", "logs", "welcome", "autorole", "levels"]
for c in core:
    bot.load_extensions(f"wolfiebot.core.{c}")

commands = ["user", "dev", "admin", "economy", "owner", "quotes"]
for c in commands:
    bot.load_extensions(f"wolfiebot.commands.{c}")

games = ["slots", "casino"]
for c in games:
    bot.load_extensions(f"wolfiebot.games.{c}")

ai = ["chat"]
for c in ai:
    bot.load_extensions(f"wolfiebot.ai.{c}")

@bot.listen(hikari.ExceptionEvent)
async def on_error(event: hikari.ExceptionEvent[EventT]) -> None:
    """
    Event listener for handling exceptions raised during event processing.

    Args:
        event: The event object representing the exception event.

    Raises:
        event.exception: The exception that occurred during event processing.

    Returns:
        None
    """
    raise event.exception

@bot.listen(lightbulb.CommandErrorEvent)
async def on_command_error(event: lightbulb.CommandErrorEvent) -> None:
    """
    Event listener for handling command errors.

    Args:
        event: The event object representing the command error event.

    Raises:
        lightbulb.NotOwner: If the user is not the owner of the command.
        lightbulb.CommandIsOnCooldown: If the command is on cooldown.

    Returns:
        None
    """
    exc = event.exception

    if isinstance(exc, lightbulb.NotOwner):
        await event.context.respond("You do not have access to this command")

    if isinstance(exc, lightbulb.CommandIsOnCooldown):
        seconds = exc.retry_after
        time = await format_time(seconds)
        await event.context.respond(f"Command is on cooldown, retry in {time}")

async def format_time(seconds):
    """
    Formats a time duration in seconds into a human-readable string.

    Args:
        seconds: The time duration in seconds.

    Returns:
        A string representing the formatted time duration.
    """
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
