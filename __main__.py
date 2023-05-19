import hikari
import lightbulb
import os
import logging

from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from hikari.events.base_events import EventT
from lightbulb.errors import ExtensionNotFound
from wolfiebot.database.database import Database

load_dotenv(find_dotenv())
log = logging.getLogger(__name__)
bot = lightbulb.BotApp(token=os.environ.get("TOKEN"), prefix="!", intents=hikari.Intents.ALL, default_enabled_guilds=1021249050445611009)
db = Database()

@bot.listen(hikari.StartedEvent)
async def start(event):
    await bot.update_presence(status=hikari.Status.ONLINE, activity=hikari.Activity( name=db.read_user_data(bot.get_me().id, "status"), type=hikari.ActivityType.PLAYING,),)

core = ["quotes", "rooms", "logs", "welcome", "autorole", "chat"]
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