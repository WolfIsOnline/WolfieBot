import hikari
import lightbulb
import logging
import wolfiebot
import requests
import json
import re
import time
import asyncio

from wolfiebot.database.database import Database

plugin = lightbulb.Plugin("core.chat")
log = logging.getLogger(__name__)
database = Database()

base_url = "http://localhost:3000"
NUM_OF_RETRIES = 20

@plugin.listener(hikari.GuildMessageCreateEvent)
async def guild_listen(event) -> None:
    if plugin.bot.get_me().id in event.message.user_mentions:
        user = plugin.bot.cache.get_member(event.guild_id, event.author.id)
        name = user.nickname
        if name is None:
            name = user
        await chat(event=event, user_name=name, user_id=user.id)
        
@plugin.listener(hikari.DMMessageCreateEvent)
async def dm_listen(event) -> None:
    if event.author_id == plugin.bot.get_me().id:
        return
    await chat(event=event, user_name=event.author, user_id=event.author.id)
    
async def chat(event, user_name: str, user_id: int) -> None:
    retries = 0
    channel = event.message.channel_id
    session_id = establish_connection(user_id=user_id, user_name=str(user_name))
    message = re.sub(r"<.*?>", "", event.message.content)
    await plugin.bot.rest.trigger_typing(channel)
    response = send_message(session_id=session_id, message=message)
    if response == "blank":
        while response == "blank":
            retries += 1
            log.warning(f"session [{session_id}] response blank retrying... {retries}")
            response = get_response(session_id=session_id)
            if retries > NUM_OF_RETRIES:
                log.warning(f"session [{session_id}] timed out after {retries} retries")
                close_session(session_id=session_id)
                return None
            time.sleep(3)
    if response == "denied":
        while response == "denied":
            retries += 1
            log.warning(f"session [{session_id}] denied message retrying...")
            response = send_message(session_id=session_id, message=message)
            if retries > NUM_OF_RETRIES:
                log.warning(f"session [{session_id}] timed out after {retries} retries")
                close_session(session_id=session_id)
                return None
            time.sleep(3)
    
    close_session(session_id=session_id)
    await plugin.bot.rest.create_message(channel, f"<@{user_id}> {response}")
    
def send_message(session_id: str, message: str) -> str:
    url = f"{base_url}/session/{session_id}/message"
    message = {"message" : message}
    response = requests.post(url, headers={"Content-Type" : "application/json"}, data=json.dumps(message))
    
    if response.status_code == 202:
        log.info(f"session [{session_id}] accepted message")
        time.sleep(3)
        _response = get_response(session_id=session_id)
    else:
        return "denied"
    return _response
    
def close_session(session_id: str) -> None:
    url = f"{base_url}/http:/session/{session_id}/close"
    response = requests.get(url, headers={}, data={})
    if response.status_code == 404:
        log.info(f"session [{session_id}] has closed")
    else:
        log.warning(f"session [{session_id}] could not close")
    
def create_session(user_id: int, user_name: str) -> str:
    url = f"{base_url}/session/open"
    post_data = {
        "uid" : str(user_id),
        "sceneId" : "workspaces/default-firdbgosgclm_v_vu5dcnw/scenes/discord",
        "characterId": "-1",
        "playerName": user_name,
    }
    
    response = requests.post(url, headers={"Content-Type" : "application/json"}, data=json.dumps(post_data))
    
    if response.status_code == 200:
        data = response.json()
        session_id = data["sessionId"]
        log.info(f"session [{session_id}] has been created")
        return session_id
    
def get_response(session_id: str) -> str:
    url = f"{base_url}/events"
    response = requests.get(url, headers={}, data={})
    data = response.json()
    messages = []
    for c in data:
        if c["sessionId"] == session_id:
            if c["type"] == "text":
                messages.append(c["text"])
            elif c["type"] == "disconnected":
                return "denied"
    message = "".join(messages)
    if message == "":
        return "blank"
    
    log.info(f"session [{session_id}] replying")
    return message
    
def establish_connection(user_id: int, user_name: str) -> str:
    session_id = create_session(user_id=user_id, user_name=user_name)
    if session_id is None:
        session_id = database.read_user_data(user_id=user_id, name="session_id")
    else:
        database.edit_user_data(user_id=user_id, name="session_id", value=session_id)
    return session_id
    
def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
