import hikari
import lightbulb
import os
import logging

from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from hikari.events.base_events import EventT
from lightbulb.errors import ExtensionNotFound

load_dotenv(find_dotenv())
log = logging.getLogger(__name__)
bot = lightbulb.BotApp(token=os.environ.get("TOKEN"), prefix="!", intents=hikari.Intents.ALL, default_enabled_guilds=1021249050445611009)

core = ["quotes", "rooms", "logs", "welcome"]
for c in core:
    bot.load_extensions(f"wolfiebot.core.{c}")

commands = ["user", "economy", "dev", "admin"]
for c in commands:
    bot.load_extensions(f"wolfiebot.commands.{c}")
        
@bot.listen(hikari.ExceptionEvent)
async def on_error(event: hikari.ExceptionEvent[EventT]) -> None:
    raise event.exception

@bot.listen(lightbulb.CommandErrorEvent)
async def on_command_error(event: lightbulb.CommandErrorEvent) -> None:
    exc = event.exception

    if isinstance(exc, lightbulb.NotOwner):
        await event.context.respond("You do not have access to this command")
        
        
    
if __name__ == "__main__":
    import uvloop
    uvloop.install()
    bot.run()