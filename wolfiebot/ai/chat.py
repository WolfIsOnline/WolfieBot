import hikari
import lightbulb
import logging
import wolfiebot
import requests
import json
import re
import time
import asyncio
import inspect
import pprint

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
    if plugin.bot.get_me().id in event.message.user_mentions:
        user = plugin.bot.cache.get_member(event.guild_id, event.author.id)
        name = user.nickname
        if name is None:
            name = user
        await chat(event=event, user_name=name, user_id=user.id, is_dm=False)
        
@plugin.listener(hikari.DMMessageCreateEvent)
async def dm_listen(event) -> None:
    if event.author_id == plugin.bot.get_me().id:
        return
    await chat(event=event, user_name=event.author, user_id=event.author.id, is_dm=True)
    
async def chat(event, user_name: str, user_id: int, is_dm: bool) -> None:
    session_id = database.read_user_data(user_id=user_id, name="session_id")
    session_status = api.get_session_status(session_id)
    if session_status is False:
        session = api.open_session(user_id=user_id, scene_id=SCENE_ID, character_id=CHARACTER_ID, player_name=str(user_name), server_id="")
        session_id = session["id"]
    
    else:
        log.info(f"session valid [{session_id}]")
        
    message = re.sub(r"<.*?>", "", event.message.content)
    if is_dm is True:
        content = f"{event.author}: {message}"
        await plugin.bot.rest.execute_webhook(webhook=int(wolfiebot.WEBHOOK_ID), token=wolfiebot.WEBHOOK_TOKEN, content=content, username="Logs")
    channel_id = event.channel_id
    await plugin.bot.rest.trigger_typing(channel_id)
    reply = api.send_message(session_id=session_id, message=message, user_id=str(user_id), scene_id=SCENE_ID, character_id=CHARACTER_ID, player_name=str(user_name), server_id="")
    if reply == "" or reply is None:
        return None
    
    state = database.read_user_data(plugin.bot.get_me().id, "voice_state")
    if state is True:
        wolfiebot.ai.voice.generate_reply(reply)
        audio = hikari.File("./WolfieBot/wolfiebot/content/reply.mp4")
        await event.app.rest.create_message(channel=channel_id, content=reply, attachment=audio, reply=event.message)
    else:
        await event.app.rest.create_message(channel=channel_id, content=reply, reply=event.message)
    if is_dm is True:
        content = f"wolfie: {reply}"
        await plugin.bot.rest.execute_webhook(webhook=int(wolfiebot.WEBHOOK_ID), token=wolfiebot.WEBHOOK_TOKEN, content=content, username="Logs")
        
    log.info(f"sending reply to session [{session_id}]")
     
def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
