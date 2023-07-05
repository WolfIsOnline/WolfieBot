"""
Welcome extension
"""
import logging
import hikari
import lightbulb

# pylint: disable=import-error, no-name-in-module
from wolfiebot.database.database import Database
from wolfiebot.ai.api import Api

log = logging.getLogger(__name__)
plugin = lightbulb.Plugin("core.welcome")
database = Database()
api = Api()

SCENE_ID = "workspaces/default-firdbgosgclm_v_vu5dcnw/scenes/discord"
CHARACTER_ID = "-1"

@plugin.listener(hikari.MemberCreateEvent)
async def user_join(event):
    """
    Handles the user join event and sends a welcome message.

    Args:
        event: The event object representing the user join event.

    Returns:
        None
    """
    user = event.user
    user_id = user.id
    guild_id = event.guild_id
    welcome_channel = database.read_guild_data(guild_id=guild_id, name="welcome_channel")
    # pylint: disable=undefined-variable
    message = await wolfiebot.ai.chat.generate_scene_reply(
        user_id=user_id,
        name=user,
        custom_id="welcome"
    )
    await plugin.bot.rest.create_message(
        channel=welcome_channel,
        content=f"<@{user_id}> {message}"
    )

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
