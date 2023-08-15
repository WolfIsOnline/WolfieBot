"""
AI Chat Module
"""

import logging
import re
import hikari
import lightbulb

# pylint: disable=import-error
# pylint: disable=no-name-in-module
from wolfiebot.database.database import Database
from wolfiebot.ai.simple_api import Simple_API

plugin = lightbulb.Plugin("ai.chat")
log = logging.getLogger(__name__)
database = Database()
simple_api = Simple_API()

SCENE_ID = "workspaces/default-firdbgosgclm_v_vu5dcnw/scenes/discord"
CHARACTER_ID = "-1"

@plugin.listener(hikari.GuildMessageCreateEvent)
async def guild_listen(event) -> None:
    """
    Listens for guild message create events and handles mentions of the bot user.

    Args:
        event (hikari.GuildMessageCreateEvent): The event object
    """
    if plugin.bot.get_me().id in event.message.user_mentions:
        user = plugin.bot.cache.get_member(event.guild_id, event.author.id)
        name = user.nickname
        if name is None:
            name = user
        await chat(event=event, username=name, user_id=user.id, is_dm=False)

@plugin.listener(hikari.DMMessageCreateEvent)
async def direct_listen(event) -> None:
    """
    Listens for direct message create events and handles messages received from users.

    Args:
        event (hikari.DMMessageCreateEvent): The event object
    """
    if event.author_id == plugin.bot.get_me().id:
        return
    await chat(event=event, username=event.author, user_id=event.author.id, is_dm=True)

async def chat(event, username: str, user_id: int, is_dm: bool) -> None:
    """
    Initiates a chat session and processes the chat response.

    Args:
        event (hikari.MessageCreateEvent): The message create event.
        username (str): The username of the user.
        user_id (int): The ID of the user.
        is_dm (bool): Indicates if the chat is in a direct message.
    """
    channel_id = event.channel_id
    session_id = database.read_user_data(user_id=user_id, name="session_id")
    character_id = database.read_user_data(user_id=user_id, name="character_id")
    message = re.sub(r"<.*?>", "", event.message.content)
    await plugin.bot.rest.trigger_typing(channel_id)
    reply = await simple_api.send_message(
        message=message,
        session_id=session_id,
        character_id=character_id
    )
    if reply.get("code") == 9 or reply.get("code") == 5:
        log.info("session invalid creating new")
        session = await simple_api.open_session({
            "user_id" : str(user_id),
            "name" : str(username),
            "gender" : "male",
            "age" : 23
        })
        session_id = session.get("name")
        character_id = session.get("sessionCharacters", [])[0].get("character", None)
        await update_session_id(user_id=user_id, session_id=session_id, character_id=character_id)
        return await chat(event, username, user_id, is_dm)
    text_list = reply.get("textList")
    combine_text = "".join(text_list)
    await event.app.rest.create_message(
        channel=channel_id,
        content=combine_text,
        reply=event.message
    )

async def update_session_id(user_id: int, session_id: str, character_id: str) -> None:
    """
    Updates the session ID and character ID for a user.

    Args:
        user_id (int): The ID of the user.
        session_id (str): The new session ID to be updated.
        character_id (str): The new character ID to be updated.
    """
    database.edit_user_data(user_id=user_id, name="session_id", value=session_id)
    database.edit_user_data(user_id=user_id, name="character_id", value=character_id)

def load(bot: lightbulb.BotApp) -> None:
    """
    Loads the plugin into the specified bot.

    Args:
        bot (lightbulb.BotApp): The bot instance to load the plugin into.
    """
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp) -> None:
    """
    Unloads the plugin from the specified bot.

    Args:
        bot (lightbulb.BotApp): The bot instance to unload the plugin from.
    """
    bot.remove_plugin(plugin)
