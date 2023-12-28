import wolfiebot
import time
import logging
import json
import lightbulb
import hikari
import asyncio

from wolfiebot.database.database import UserData
from datetime import datetime

import openai
from openai import OpenAI

log = logging.getLogger(__name__)


class AIManager:
    def __init__(self, user_id):
        self.client = OpenAI(api_key=wolfiebot.OPENAI_API_KEY)
        self.user_data = UserData(user_id=user_id)
        self.thread_id = self.user_data.retrieve(name="thread_id")
        self.user_id = user_id
        self.function_table = {
            "_write_to_brain" : self._write_to_brain,
            "_retrieve_from_brain" : self._retrieve_from_brain,
            "_delete_from_brain" : self._delete_from_brain
        }

        if self.thread_id is None:
            self.thread_id = self._create_thread()

    async def send_message(self, text: str):
        try:
            message = await self._add_message(message=text)
            run = await self._run_reply()
        except openai.BadRequestError:
            log.warning(e.message)
            return None

        reply_json = await self._get_reply(message)
        reply = self._parse_reply(reply_json)[0]
        return reply

    async def _add_message(self, message):
        message = self.client.beta.threads.messages.create(
            thread_id=self.thread_id, role="user", content=message
        )
        return message

    async def _get_reply(self, message):
        reply = self.client.beta.threads.messages.list(
            thread_id=self.thread_id, order="asc", after=message.id
        )
        return self._load_json(reply)


    async def _run_reply(self):
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread_id, assistant_id=wolfiebot.ASSISTANT_ID
        )

        while run.status == "queued" or run.status == "in_progress":
            run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread_id,
                run_id=run.id
            )

            await asyncio.sleep(.5)
            log.info(f"run.status: {run.status}")

            if run.status == "requires_action":
                tool_calls = run.required_action.submit_tool_outputs.model_dump()
                tool_output = []

                for call in tool_calls["tool_calls"]:
                    function_name = call["function"]["name"]
                    arguments = json.loads(call["function"]["arguments"])

                    table = self.function_table.get(function_name)
                    if table:
                        result = table(**arguments)
                        output = json.dumps() if not isinstance(result, str) else result
                        tool_output.append({
                            "tool_call_id": call["id"],
                            "output": output
                        })
                        log.info(f"function_called: {function_name}")
                        log.info(f"function_arguments: {arguments}")
                    else:
                        log.info(f"Function {function_name} not found")

                    run = self.client.beta.threads.runs.submit_tool_outputs(
                        thread_id=self.thread_id,
                        run_id=run.id,
                        tool_outputs=tool_output
                    )
        return run

    def _create_thread(self):
        thread = self.client.beta.threads.create()
        self.user_data.edit("thread_id", thread.id)
        return thread.id

    def _parse_reply(self, data):
        values = []
        for data_item in data["data"]:
            if "content" in data_item:
                for content_item in data_item["content"]:
                    if "text" in content_item and "value" in content_item["text"]:
                        values.append(content_item["text"]["value"])
        return values

    def _load_json(self, data):
        return json.loads(data.model_dump_json())

    def _write_to_brain(self, data_name: str, data_value: str):
        self.user_data._ai_edit(data_name, data_value)
        return f"{data_name} : {data_value} has been stored for later access"

    def _retrieve_from_brain(self):
        data = self.user_data._ai_retrieve()
        return f"here is the information in your brain: {data}"

    def _delete_from_brain(self, data_name: str):
        self.user_data._ai_delete(data_name)
        return f"{data_name} has been removed"
