"""
Auto Roles. Automatically assign roles upon joining the server
"""

import logging
import hikari
import lightbulb

# pylint: disable=no-name-in-module, import-error
from wolfiebot.database.database import Database

log = logging.getLogger(__name__)
plugin = lightbulb.Plugin("core.autorole")
database = Database()

@plugin.listener(hikari.MemberCreateEvent)
async def user_join(event):
    """
    Handle user join event.

    Assigns autoroles to a newly joined member, if any are configured for the guild.

    Args:
        event (hikari.MemberCreateEvent): The member create event object.

    Returns:
        None
    """
    user = event.member
    guild_id = event.guild_id
    roles = database.read_guild_data(guild_id, "autoroles")
    if roles is not None:
        for _role in roles:
            role = plugin.bot.cache.get_role(_role)
            await user.add_role(role)

def load(bot: lightbulb.BotApp):
    """
    Loads the plugin into the bot.

    Parameters:
    - bot (lightbulb.BotApp): The bot instance.

    """
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp):
    """
    Unloads the plugin from the specified bot.

    Args:
        bot (lightbulb.BotApp): The bot instance to unload the plugin from.

    Returns:
        None
    """
    bot.remove_plugin(plugin)
