import os
import logging

from dotenv import load_dotenv, find_dotenv
from pymongo import ASCENDING, MongoClient
from pymongo.errors import CollectionInvalid
from pymongo.errors import DuplicateKeyError

log = logging.getLogger("rich")

class Guild_DataBase:
    def __init__(self):
        load_dotenv(find_dotenv())
        MONGODB_CONNECTION = os.environ.get("MONGODB_CONNECTION")
        self.client = MongoClient(MONGODB_CONNECTION)

    def add_guild(self, guild_id):
        try:
            self.client.guilds.create_collection(str(guild_id))
            log.info(f"{guild_id} has been added")
        except CollectionInvalid:
            log.info(f"{guild_id} already exists")
    
    def update_guild_key(self, guild_id, id, value):
        document = self.client["guilds"][str(guild_id)]
        document.find_one_and_update({"_id": id},{"$set": {"value": value}},upsert=True)

    def add_guild_key(self, guild_id, id, value):
        try:
            document = self.client["guilds"][str(guild_id)]
            data = {"_id": id, "value": value}
            document.insert_one(data)
        except DuplicateKeyError:
            log.info(f"{id} is a duplicate")

    def get_guild_key(self, guild_id, id):
        document = self.client["guilds"][str(guild_id)]
        results = document.find({"_id":id})
        value = "None"
        for x in results:
            value = x["value"]
        return value