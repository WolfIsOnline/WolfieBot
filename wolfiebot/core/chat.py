import hikari
import lightbulb
import logging
import wolfiebot
import requests
import json
import re
import time

from wolfiebot.database.database import Database

plugin = lightbulb.Plugin("core.chat")
log = logging.getLogger(__name__)
database = Database()

base_url = "http://localhost:3000"

@plugin.listener(hikari.GuildMessageCreateEvent)
async def guild_listen(event):
    if plugin.bot.get_me().id in event.message.user_mentions:
        user = plugin.bot.cache.get_member(event.guild_id, event.author.id)
        name = user.nickname
        if name is None:
            name = user
        await chat(event=event, user_name=name, user_id=user.id)
        
@plugin.listener(hikari.DMMessageCreateEvent)
async def dm_listen(event):
    if event.author_id == plugin.bot.get_me().id:
        return
    await chat(event=event, user_name=event.author, user_id=event.author.id)
    
async def chat(event, user_name: str, user_id: int):
        channel = event.message.channel_id
        session_id = establish_connection(user_id=user_id, user_name=str(user_name))
        message = re.sub(r"<.*?>", "", event.message.content)
        send_message(session_id=session_id, message=message)
        await plugin.bot.rest.trigger_typing(channel)
        time.sleep(3)
        response = get_response(session_id=session_id)
        close_connection(session_id=session_id)
        await plugin.bot.rest.create_message(channel, response)
    
def send_message(session_id: str, message: str):
    url = f"{base_url}/session/{session_id}/message"
    message = {"message" : message}
    response = requests.post(url, headers={"Content-Type" : "application/json"}, data=json.dumps(message))
    
    if response.status_code == 202:
        log.info(f"message [{message}] sent successfully")
    else:
        log.error(f"message failed to send: {response.text}")
    
def close_connection(session_id: str):
    url = f"{base_url}/http:/session/{session_id}/close"
    response = requests.get(url, headers={}, data={})
    log.info("connection closed")
    
def create_session(user_id: int, user_name: str) -> str:
    url = "http://localhost:3000/session/open"
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
        
        return session_id
    
def get_response(session_id: str):
    url = f"{base_url}/events"
    response = requests.get(url, headers={}, data={})
    data = response.json()
    messages = []
    for c in data:
        if c["sessionId"] == session_id:
            messages.append(c["text"])
    message = "".join(messages)
    log.info(f"reply {message}")
    log.info(f"{data}")
    return message
    
def establish_connection(user_id: int, user_name: str) -> str:
    session_id = create_session(user_id=user_id, user_name=user_name)
    if session_id is None:
        session_id = database.read_user_data(user_id=user_id, name="session_id")
    else:
        log.info(f"connection established: {session_id}")
        database.edit_user_data(user_id=user_id, name="session_id", value=session_id)
    return session_id
    
def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
