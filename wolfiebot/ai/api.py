import requests
import json
import time
import logging

from typing import List
from wolfiebot.database.database import Database

host = "http://localhost:3000"
log = logging.getLogger(__name__)

SCENE_ID = "workspaces/default-firdbgosgclm_v_vu5dcnw/scenes/discord"
CHARACTER_ID = "-1" 



class Api:
    def __init__(self):
        self.database = Database()
    
    def get_server_status(self) -> str:
        response = requests.get(url=f"{host}/status", headers={}, data={})
        return response.text
    
    def open_session(self, user_id: str, scene_id: str, character_id: str, player_name: str, server_id: str) -> List[str]:
        response = requests.post(url=f"{host}/session/open", headers={"Content-Type" : "application/json"}, data=json.dumps({"uid" : str(user_id), "sceneId" : scene_id, "playerName" : player_name, "serverId" : server_id}))
        if response.status_code == 200:
            data = response.json()
            session = {"id" : data["sessionId"], "character" : data["character"], "characters" : data["characters"]}
            session_id = data["sessionId"]
            self.update_session_id(user_id=user_id, session_id=session_id)
            log.info(f"opening session [{session_id}]")
        else:
            session = {"id" : response.status_code, "character" : response.status_code, "characters" : response.status_code}
            log.error(f"{response.text} {response.status_code}")
        return session
    
    def close_session(self, session_id: str) -> bool:
        response = requests.get(url=f"{host}/session/{session_id}/close", headers={}, data={})
        if response.status_code == 200:
            return True
        return False
    
    def get_session_status(self, session_id: str) -> bool:
        response = requests.get(url=f"{host}/session/{session_id}/status", headers={}, data={})
        if response.status_code == 404:
            return False
        return True
    
    def send_message(self, session_id: str, message: str, user_id: str, scene_id: str, character_id: str, player_name: str, server_id: str) -> str:
        response = requests.post(url=f"{host}/session/{session_id}/message", headers={"Content-Type" : "application/json"}, data=json.dumps({"message": message}))
        if response.status_code == 202:
            time.sleep(3)
            reply = self._get_response(session_id=session_id, _message=message)
            if reply == "disconnected":
                log.warning(f"message failed, retrying {reply}")
                status = self.get_session_status(session_id=session_id)
                if status is False:
                    session = self.open_session(user_id=user_id, scene_id=scene_id, character_id=character_id, player_name=player_name, server_id=server_id)
                    session_id = session["id"]
                    return self.send_message(session_id=session_id, message=message, user_id=str(user_id), scene_id=SCENE_ID, character_id=CHARACTER_ID, player_name=player_name, server_id="")
            return reply
        
        
    def _get_response(self, session_id: str, _message: str = "", attempts: int = 10, _attempt: int = 1) -> str:
        response = requests.get(url=f"{host}/events", headers={}, data={})
        data = response.json()
        messages = []
        
        for c in data:
            if c["sessionId"] == session_id:
                if c["type"] == "text":
                    messages.append(c["text"])
                elif c["type"] == "disconnected":
                    return "disconnected"
                
        message = "".join(messages)
        
        if message == "":
            if _attempt <= attempts:
                log.warning(f"message is empty, retrying ({_attempt}/{attempts})")
                time.sleep(2)
                return self._get_response(session_id=session_id, attempts=attempts, _attempt=_attempt + 1)
        log.info(f"reply generated [{session_id}]")
        return message
    
    def update_session_id(self, user_id: int, session_id: str):
        if session_id is None or session_id == 409:
            return
        self.database.edit_user_data(user_id=int(user_id), name="session_id", value=session_id)