import logging
import hikari
import lightbulb

# pylint: disable=no-name-in-module, import-error, unused-import
from wolfiebot.database.database import Database

log = logging.getLogger(__name__)
plugin = lightbulb.Plugin("core.stats")
database = Database()

@plugin.listener(hikari.GuildMessageCreateEvent)
async def listen(event):
    if event.is_bot is True or event.message.content.startswith("!"):
        return

    user_id = event.author.id
    messages = database.read_user_data(user_id, "messages")
    if messages is None:
        messages = 0
    messages += 1
    database.edit_user_data(user_id, "messages", messages)

async def get_all_messages(user_id):
    pass

def load(bot: lightbulb.BotApp) -> None:
    """
    Loads the plugin into the bot.

    Args:
        bot (lightbulb.BotApp): The bot instance.

    Returns:
        None
    """
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp) -> None:
    """
    Unloads the plugin from the bot.

    Args:
        bot (lightbulb.BotApp): The bot instance.

    Returns:
        None
    """
    bot.remove_plugin(plugin)
