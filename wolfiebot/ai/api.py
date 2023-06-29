"""
Inworld API Wrapper Module
"""

import json
import time
import logging
from typing import Dict, Optional, TypedDict
import requests

# pylint: disable=import-error
from wolfiebot.database.database import Database

log = logging.getLogger(__name__)
database = Database()

HOST = "http://localhost:3000"
SCENE_ID = "workspaces/default-firdbgosgclm_v_vu5dcnw/scenes/discord"
CHARACTER_ID = "-1"


class OpenSessionData(TypedDict):
    """
    Represents data for opening a session.

    Attributes:
        user_id (int): The ID of the user associated with the session.
        scene_id (str): The ID of the scene for the session.
        character_id (str, optional): The ID of the character for the session. Default is "-1".
        name (str, optional): The name of the player associated with the session. Default is an empty string.
        server_id (str, optional): The ID of the server associated with the session. Default is an empty string.
    """
    user_id: int
    scene_id: str
    character_id: str = "-1"
    name: Optional[str] = ""
    server_id: Optional[str] = ""


class Api:
    """
    Serves as an interface for interacting with the api.

    Note:
        Before using the Api class, make sure to run the proxy server.

    Attributes:
        HOST (str): The base URL of the proxy server.
        log (logging.Logger): The logger instance for logging messages.
        database (Database): An instance of the Database class for accessing and writing user data.
        SCENE_ID (str): The default scene ID for opening a session.
        CHARACTER_ID (str): The default character ID for opening a session.
    """

    def get_server_status(self) -> str:
        """
        Retrieves the status of the proxy server.

        Returns:
            str: The server status response as a string.

        Raises:
            requests.exceptions.RequestException: If an error occurs during the request.
            TimeoutError: If the request times out after 10 seconds.
        """
        response = requests.get(
            url=f"{HOST}/status",
            headers={},
            data={},
            timeout=10
        )
        return response.text

    def open_session(self, data: OpenSessionData) -> Dict[str, any]:
        """
        Opens a session for the specified user and returns session information.

        Args:
            data (OpenSessionData): A dictionary containing the following keys:
                - user_id (int): The ID of the user associated with the session.
                - scene_id (str): The ID of the scene for the session.
                - character_id (str): The ID of the character for the session.
                - name (str, optional): The name of the player associated with the session.
                - server_id (str, optional): The ID of the server associated with the session.

        Returns:
            dict: A dictionary containing session information in the following format:
                {
                    "id": str,            # The session ID
                    "character": any,     # The character associated with the session
                    "characters": any     # The list of available characters
                }

        Raises:
            KeyError: If any of the required keys (user_id, scene_id, name) is missing.
            requests.exceptions.RequestException: If an error occurs during the request.
            TimeoutError: If the request times out after 10 seconds.
        """
        required = ["user_id", "scene_id", "character_id"]
        if not all(key in data for key in required):
            raise KeyError("Missing required keys in the data dictionary.")

        name = data.get("name")
        server_id = data.get("server_id")
        user_id = data.get("user_id")

        if name is None:
            name = ""
        if server_id is None:
            server_id = ""

        response = requests.post(
            url=f"{HOST}/session/open",
            headers={"Content-Type": "application/json"},
            data=json.dumps({
                "uid": str(user_id),
                "sceneId": data.get("scene_id"),
                "characterId": data.get("character_id"),
                "playerName": name,
                "serverId": server_id
            }),
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            session = {
                "id": data.get("sessionId"),
                "character": data.get("character"),
                "characters": data.get("characters")
            }
            session_id = session.get("id")
            log.info(data.get("user_id"))
            self.update_session_id(user_id=user_id, session_id=session_id)
            log.info("Opening session [%s]", session_id)
        else:
            session = {
                "id": response.status_code,
                "character": response.status_code,
                "characters": response.status_code
            }

        return session


    def close_session(self, session_id: str) -> bool:
        """
        Closes the specified session.

        Args:
            session_id (str): The ID of the session to be closed.

        Returns:
            bool: True if the session was closed successfully, False otherwise.

        Raises:
            requests.exceptions.RequestException: If an error occurs during the request.
            TimeoutError: If the request times out after 10 seconds.
        """
        response = requests.get(
            url=f"{HOST}/session/{session_id}/close",
            headers={},
            data={},
            timeout=10
        )
        if response.status_code == 200:
            return True
        return False

    def get_session_status(self, session_id: str) -> bool:
        """
        Retrieves the status of the specified session.

        Args:
            session_id (str): The ID of the session.

        Returns:
            bool: True if the session exists, False otherwise.

        Raises:
            requests.exceptions.RequestException: If an error occurs during the request.
            TimeoutError: If the request times out after 10 seconds.
        """
        response = requests.get(
            url=f"{HOST}/session/{session_id}/status",
            headers={},
            data={},
            timeout=10
        )
        if response.status_code == 404:
            return False
        return True

    def send_message(self, session_id: str, message: str, data: OpenSessionData) -> str:
        """
        Sends a message to the specified session and retrieves the response.

        Args:
            session_id (str): The ID of the session.
            message (str): The message to be sent.
            data (OpenSessionData): The data containing session information.
                - user_id (int): The ID of the user associated with the session.
                - scene_id (str): The ID of the scene for the session.
                - character_id (str): The ID of the character for the session.
                - name (str, optional): The name of the player associated with the session.
                - server_id (str, optional): The ID of the server associated with the session.

        Returns:
            str: The response message from the session.

        Raises:
            requests.exceptions.RequestException: If an error occurs during the request.
            TimeoutError: If the request times out after 10 seconds.
        """
        response = requests.post(
            url=f"{HOST}/session/{session_id}/message",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"message": message}),
            timeout=10
        )

        if response.status_code == 202:
            time.sleep(3)
            reply = self._get_response(session_id=session_id, _message=message)
            if reply == "disconnected":
                log.warning("message failed, retrying %s", reply)
                status = self.get_session_status(session_id=session_id)
                if status is False:
                    session_data = {
                        "user_id": data.get("user_id"),
                        "scene_id": data.get("scene_id"),
                        "character_id": data.get("character_id"),
                        "player_name": data.get("player_name"),
                        "server_id": data.get("server_id")
                    }
                    session = self.open_session(session_data)
                    session_id = session.get("id")
                    return self.send_message(
                        session_id=session_id, message=message, data=session_data)
            return reply
        return None

    def update_session_id(self, user_id: int, session_id: str) -> None:
        """
        Updates the session ID for a user in the database.

        Args:
            user_id (int): The ID of the user.
            session_id (str): The session ID to be updated.

        Returns:
            None

        Notes:
            If the session ID is None or equals 409, the function returns immediately without making any changes.
            This is to avoid the problem of incorrectly setting the session id to none or 409.
            This is techically a work-around to a bigger issue but it works for now.
        """
        if session_id is None or session_id == 409:
            return
        database.edit_user_data(user_id=user_id, name="session_id", value=session_id)

    def _get_response(
        self,
        session_id: str,
        _message: str = "",
        attempts: int = 10,
        _attempt: int = 1
    ) -> str:
        response = requests.get(
            url=f"{HOST}/events",
            headers={},
            data={},
            timeout=10
        )
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
                log.warning("message is empty, retrying (%s/%s)",
                            _attempt, attempts)
                time.sleep(2)
                return self._get_response(
                    session_id=session_id,
                    attempts=attempts,
                    _attempt=_attempt + 1
                )

        log.info("reply generated [%s]", session_id)
        return message
