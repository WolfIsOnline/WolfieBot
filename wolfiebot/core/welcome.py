"""
Welcome extension
"""
import logging
import hikari
import lightbulb

# pylint: disable=import-error, no-name-in-module
from wolfiebot.database.database import Database
from wolfiebot.ai.simple_api import Simple_API

log = logging.getLogger(__name__)
plugin = lightbulb.Plugin("core.welcome")
database = Database()
simple_api = Simple_API()

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

    session = await simple_api.open_session({
        user_id: user_id
    })
    session_id = session.get("name")
    character_id = session.get("sessionCharacters", [])[0].get("character", None)

    response = await simple_api.send_trigger_message(
        session_id=session_id,
        character_id=character_id,
        trigger="welcome"
    )

    text_list = response.get("textList")
    combine_text = "".join(text_list)

    await plugin.bot.rest.create_message(
        channel=welcome_channel,
        content=f"<@{user_id}> {combine_text}"
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
