"""
AI Chat Module
"""

import logging
import hikari
import lightbulb

# pylint: disable=import-error
# pylint: disable=no-name-in-module
import wolfiebot
from wolfiebot.database.database import Database
from wolfiebot.ai.api import Api

plugin = lightbulb.Plugin("ai.chat")
log = logging.getLogger(__name__)
database = Database()
api = Api()

SCENE_ID = "workspaces/default-firdbgosgclm_v_vu5dcnw/scenes/discord"
CHARACTER_ID = "-1"

@plugin.listener(hikari.GuildMessageCreateEvent)
async def guild_listen(event) -> None:
    """
    Listens for guild message create events and handles mentions of the bot user.

    Args:
        event (hikari.GuildMessageCreateEvent): The event object

    Returns:
        None
    """
    if plugin.bot.get_me().id in event.message.user_mentions:
        user = plugin.bot.cache.get_member(event.guild_id, event.author.id)
        name = user.nickname
        if name is None:
            name = user
        await chat(event=event, user_name=name, user_id=user.id, is_dm=False)

@plugin.listener(hikari.DMMessageCreateEvent)
async def direct_listen(event) -> None:
    """
    Listens for direct message create events and handles messages received from users.

    Args:
        event (hikari.DMMessageCreateEvent): The event object

    Returns:
        None
    """
    if event.author_id == plugin.bot.get_me().id:
        return
    await chat(event=event, user_name=event.author, user_id=event.author.id, is_dm=True)

async def chat(event, user_name: str, user_id: int, is_dm: bool) -> None:
    """
    Handles the chat functionality by sending and receiving messages in a session.

    Args:
        event: The event object representing the chat event.
        user_name (str): The name of the user associated with the chat.
        user_id (int): The ID of the user associated with the chat.
        is_dm (bool): Indicates whether the chat is in a direct message or not.

    Returns:
        None

    Raises:
        None
    """
    session_id = database.read_user_data(user_id=user_id, name="session_id")
    session_status = api.get_session_status(session_id)

    if session_status is False:
        session = api.open_session({
            "user_id": user_id,
            "scene_id": SCENE_ID,
            "character_id": CHARACTER_ID,
            "name": str(user_name)
        })

        session_id = session["id"]
    else:
        log.info("session valid [%s]", session_id)

    message = event.message.content

    if is_dm:
        content = f"{event.author}: {message}"
        await plugin.bot.rest.execute_webhook(
            webhook=int(wolfiebot.WEBHOOK_ID),
            token=wolfiebot.WEBHOOK_TOKEN,
            content=content,
            username="Logs"
        )

    channel_id = event.channel_id
    await plugin.bot.rest.trigger_typing(channel_id)
    reply = api.send_message(
        session_id=session_id,
        message=message,
        data={
            "user_id": str(user_id),
            "scene_id": SCENE_ID,
            "character_id": CHARACTER_ID,
            "name": str(user_name)
        }
    )

    if not reply:
        return None

    state = database.read_user_data(plugin.bot.get_me().id, "voice_state")
    if state:
        ## pylint: disable=no-member
        wolfiebot.ai.voice.generate_reply(reply)
        audio = hikari.File("./WolfieBot/wolfiebot/content/reply.mp4")
        await event.app.rest.create_message(
            channel=channel_id,
            content=reply,
            attachment=audio,
            reply=event.message
        )
    else:
        await event.app.rest.create_message(channel=channel_id, content=reply, reply=event.message)

    if is_dm:
        content = f"wolfie: {reply}"
        await plugin.bot.rest.execute_webhook(
            webhook=int(wolfiebot.WEBHOOK_ID),
            token=wolfiebot.WEBHOOK_TOKEN,
            content=content,
            username="Logs"
        )

    log.info("sending reply to session [%s]", session_id)

async def generate_scene_reply(user_id: int, name: str, custom_id: str):
    """
    Generate a reply for a scene interaction.

    Generates a reply for a scene interaction by opening a session, setting the user ID,
    scene ID, character ID, and name, and sending a scene trigger with the specified custom ID.
    If the user has an existing session, it will be closed before opening a new one.

    Args:
        user_id (int): The ID of the user.
        name (str): The name to set for the session.
        custom_id (str): The custom ID for the scene trigger.

    Returns:
        str: The response message
    """
    session_id = database.read_user_data(user_id=user_id, name="session_id")
    session_status = api.get_session_status(session_id)
    if session_status is True:
        api.close_session(session_id=session_id)

    session = api.open_session({
            "user_id": user_id,
            "scene_id": SCENE_ID,
            "character_id": CHARACTER_ID,
            "name": str(name)
        })
    session_id = session.get("id")
    message = api.send_scene_trigger(session_id=session_id, custom_id=custom_id)
    return message

def load(bot: lightbulb.BotApp) -> None:
    """
    Loads the plugin into the specified bot.

    Args:
        bot (lightbulb.BotApp): The bot instance to load the plugin into.

    Returns:
        None
    """
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp) -> None:
    """
    Unloads the plugin from the specified bot.

    Args:
        bot (lightbulb.BotApp): The bot instance to unload the plugin from.

    Returns:
        None
    """
    bot.remove_plugin(plugin)
