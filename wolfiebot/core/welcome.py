"""
Welcome extension
"""
import logging
import hikari
import lightbulb
import wolfiebot

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
    user = event.user
    user_id = user.id
    guild_id = event.guild_id
    welcome_channel = database.read_guild_data(guild_id=guild_id, name="welcome_channel")
    session_id = database.read_user_data(user_id=user_id, name="session_id")
    session_status = api.get_session_status(session_id)
    if session_status is True:
        api.close_session(session_id=session_id)

    session = api.open_session({
            "user_id": user_id,
            "scene_id": SCENE_ID,
            "character_id": CHARACTER_ID,
            "name": str(user)
        })
    session_id = session.get("id")
    welcome_message = api.send_scene_trigger(session_id=session_id, custom_id="welcome")
    await plugin.bot.rest.create_message(channel=welcome_channel, content=f"<@{user_id}> {welcome_message}")

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
