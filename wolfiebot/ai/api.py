import requests
import json
import time
import logging

from typing import List

host = "http://localhost:3000"
log = logging.getLogger(__name__)

class Api:
    def __init__(self):
        pass
    
    def get_server_status(self) -> str:
        response = requests.get(url=f"{host}/status", headers={}, data={})
        return response.text
    
    def open_session(self, user_id: str, scene_id: str, character_id: str, player_name: str, server_id: str) -> List[str]:
        response = requests.post(url=f"{host}/session/open", headers={"Content-Type" : "application/json"}, data=json.dumps({"uid" : user_id, "sceneId" : scene_id, "playerName" : player_name, "serverId" : server_id}))
        if response.status_code == 200:
            data = response.json()
            session = {"id" : data["sessionId"], "character" : data["character"], "characters" : data["characters"]}
        
        else:
            session = {"id" : response.status_code, "character" : response.status_code, "characters" : response.status_code}
        return session
    
    def close_session(self, session_id: str) -> bool:
        response = requests.get(url=f"{host}/session/{session_id}/close", headers={}, data={})
        
        if response.status_code == 200:
            return True
        return False
    
    def get_session_status(self, session_id: str):
        response = requests.get(url=f"{host}/session/{session_id}/status", headers={}, data={})
        
        if response.status_code == 404:
            return False
        return True
    
    def send_message(self, session_id: str, message: str, attempts: int = 3, _attempt: int = 1) -> str:
        response = requests.post(url=f"{host}/session/{session_id}/message", headers={"Content-Type" : "application/json"}, data=json.dumps({"message": message}))
        if response.status_code == 202:
            time.sleep(3)
            reply = self._get_response(session_id=session_id)
            return reply
        
        if response.status_code == 200:
            if _attempt <= attempts:
                log.warning(f"message failed, retrying ({_attempt}/{attempts})")
                time.sleep(3)
                return self.send_message(session_id=session_id, message=message, attempts=attempts, _attempt=_attempt + 1)
        return response.text
    
    def _get_response(self, session_id: str, attempts: int = 10, _attempt: int = 1) -> str:
        response = requests.get(url=f"{host}/events", headers={}, data={})
        data = response.json()
        messages = []
        
        for c in data:
            if c["sessionId"] == session_id:
                if c["type"] == "text":
                    messages.append(c["text"])
        message = "".join(messages)
        
        if message == "":
            if _attempt <= attempts:
                log.warning(f"message is empty, retrying ({attempt}/{attempts})")
                time.sleep(1)
                return self._get_response(session_id=session_id, attempts=attempts, _attempt=_attempt + 1)
        log.info(f"reply generated [{session_id}]")
        return message