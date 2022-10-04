import os
import logging
import uuid

from dotenv import load_dotenv, find_dotenv
from pymongo import ASCENDING, MongoClient
from pymongo.errors import CollectionInvalid
from pymongo.errors import DuplicateKeyError
from requests import delete
from datetime import datetime, timezone
from rich.progress import track
from rich import print
from rich import pretty



log = logging.getLogger("rich")
class _User_Database:
    def __init__(self):
        load_dotenv(find_dotenv())
        MONGODB_CONNECTION = os.environ.get("MONGODB_CONNECTION")
        self.client = MongoClient(MONGODB_CONNECTION)

    def add_transaction(self, user_id, amount, reason, _type, member):
        document = self.client["users"][str(user_id)]
        transaction_id = uuid.uuid1()
        #data = {"_id" : "transactions", "transactions" : { str(transaction_id) : {"reason" : reason, "date" : "date"}}}
        #document.insert_one({"_id" : [{str(transaction_id) : {"transaction_id" : str(transaction_id), "reason" : str(reason), "date" : datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}}]})
        data = {"$set" : { f"{transaction_id}" : {"transaction_id" : str(transaction_id), "amount" : str(amount), "reason" : str(reason), "date" : datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), "type" : _type, "member" : member}}}
        document.find_one_and_update({"_id": "transactions"}, data, upsert=True)
        return transaction_id

    def get_transaction(self, user_id):
        document = self.client["users"][str(user_id)]
        try:
            results = document.find_one({"_id" : "transactions"})
            ids = []
            transactions = []
            for id in results:
                if id == "_id":
                    continue
                ids.append(id)
            for c in document.find({"_id" : "transactions"}):
                for b in ids:
                    transactions.append(c[b])
            return transactions
        except:
            return None
            
    def add_user(self, user_id):
        try:
            self.client.users.create_collection(str(user_id))
            log.info(f"{user_id} has been added")
        except CollectionInvalid:
            log.info(f"{user_id} already exists")

    def update_user_key(self, user_id, id, value):
        document = self.client["users"][str(user_id)]
        document.find_one_and_update(
            {
                "_id": str(id)
            },
            {
                "$set":
                {
                    "value": str(value)
                }
            },
            upsert=True)


    def add_user_key(self, user_id, id, value):
        try:
            document = self.client["users"][str(user_id)]
            data = {"_id": str(id), "value": str(value)}
            document.insert_one(data)
            log.info(f"{id} has been added")

        except DuplicateKeyError:
            log.info(f"{id} is a duplicate")

    def delete_user_key(self, user_id, key_id, value):
        document = self.client["users"][str(user_id)]
        document.find_one_and_delete({"_id": key_id},{"value": value})
        log.info(f"{key_id} has been deleted")

    def get_user_key(self, user_id, id):
        document = self.client["users"][str(user_id)]
        results = document.find({"_id":str(id)})
        value = "None"
        for x in results:
            value = x["value"]
        return value

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
        document.find_one_and_update({"_id": str(id)},{"$set": {"value": str(value)}},upsert=True)

    def add_guild_key(self, guild_id, id, value):
        try:
            document = self.client["guilds"][str(guild_id)]
            data = {"_id": str(id), "value": str(value)}
            document.insert_one(data)
            log.info(f"{id} has been added")

        except DuplicateKeyError:
            log.info(f"{id} is a duplicate")

    def delete_guild_key(self, guild_id, id, value):
        document = self.client["guilds"][str(guild_id)]
        document.find_one_and_delete({"_id": id},{"value": value})
        log.info(f"{id} has been deleted")

    def get_guild_key(self, guild_id, id):
        document = self.client["guilds"][str(guild_id)]
        results = document.find({"_id":str(id)})
        value = "None"
        for x in results:
            value = x["value"]
        return value



def test_prgram():
    db = _User_Database()
    while True:
        print("1) Add Transaction")
        print("2) Add x100 Transactions")
        print("3) Add x1000 Transactions")
        print("4) Get Transaction")
        print("5) Exit")

        option = input()
        user_id = "902399559567806524"

        if option  == "1":
            db.add_transaction(user_id, "1000000","simulated transaction", "incoming", "member")
        elif option == "2":
            for c in track(range(100), description="simulating transactions"):
                db.add_transaction(user_id, "1000000","simulated transaction", "incoming", "member")
        elif option == "3":
            for c in track(range(1000), description="simulating transactions"):
                db.add_transaction(user_id, "1000000","simulated transaction", "incoming", "member")
        elif option == "4":
            db.get_transaction(user_id)
        elif option == "5":
            exit()

#test_prgram()
