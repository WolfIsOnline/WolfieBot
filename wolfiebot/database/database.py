"""
DATABASE
"""
import logging
from pymongo import MongoClient
# pylint: disable=no-name-in-module, import-error
import wolfiebot

log = logging.getLogger(__name__)

class Database:
    """
    A class for interacting with a database.

    This class provides functions for managing user and guild data in the database.

    Attributes:
        client: The database client instance.
    """
    def __init__(self):
        """
        Initializes a new instance.

        """
        self.client = MongoClient(wolfiebot.MONGODB_CONNECTION)

    def edit_user_data(self, user_id, name, value):
        """
        Edits user data with the specified name and value.

        Args:
            user_id (str): The ID of the user.
            name (str): The name of the data to edit.
            value: The new value to set.
        """
        document = self.client["wolfie"]["users"]
        document.find_one_and_update({"_id": user_id}, {"$set" : { name : value }}, upsert=True)

    def append_user_data(self, user_id, name, value):
        """
        Appends data to a user's data with the specified name.

        Args:
            user_id (str): The ID of the user.
            name (str): The name of the data to append.
            value: The value to append.

        """
        document = self.client["wolfie"]["users"]
        document.find_one_and_update({"_id" : user_id}, {"$push" : { name : value }}, upsert=True)

    # this is to long but is very specific
    # never use this unless you have no choice
    def remove_user_data_array_by_index(self, user_id, name, index):
        """
        Removes an element from a user's data array by index.

        Args:
            user_id (str): The ID of the user.
            name (str): The name of the data array.
            index (int): The index of the element to remove.
        """
        document = self.client["wolfie"]["users"]

        # this is a work around for removing an array by the index
        # this can cause some future issues but for now it works
        document.find_one_and_update({"_id" : user_id}, {"$unset": {f"{name}.{index}": 1}}, upsert=True)
        document.find_one_and_update({"_id" : user_id}, {"$pull" : {f"{name}" : None}}, upsert=True)

    def read_user_data(self, user_id, name=None):
        document = self.client["wolfie"]["users"]
        raw_data = document.find({"_id" : user_id}, {})
        for data in raw_data:
            if name is not None:
                is_present = name in data
                if is_present is False:
                    return None
                return data[name]
        return None

    def delete_user_data(self, user_id, name):
        """
        Deletes user data with the specified name.

        Args:
            user_id (str): The ID of the user.
            name (str): The name of the data to delete.

        """
        document = self.client["wolfie"]["users"]
        document.update_one({"_id" : user_id}, { "$unset" : { name : {} } })

    def edit_guild_data(self, guild_id, name, value):
        """
        Edits guild data with the specified name and value.

        Args:
            guild_id (str): The ID of the guild.
            name (str): The name of the data to edit.
            value: The new value to set.

        """
        document = self.client["wolfie"]["guilds"]
        document.find_one_and_update({"_id": guild_id}, {"$set" : { name : value }}, upsert=True)

    def append_guild_data(self, guild_id, name, value):
        """
        Appends data to a guild with the specified name.

        Args:
            guild_id (str): The ID of the guild.
            name (str): The name of the data to append.
            value: The value to append.

        """
        document = self.client["wolfie"]["guilds"]
        document.find_one_and_update({"_id" : guild_id}, {"$push" : { name : value }}, upsert=True)

    def remove_guild_data_array(self, guild_id, name, value):
        """
        Removes a value from an array in guild data.

        Args:
            guild_id (str): The ID of the guild.
            name (str): The name of the data array.
            value: The value to remove from the array.

        """
        document = self.client["wolfie"]["guilds"]
        document.find_one_and_update({"_id" : guild_id}, {"$pull" : { name : value }}, upsert=True)

    def read_guild_data(self, guild_id, name=None):
        """
        Reads guild data or a specific named data from the guild.

        Args:
            guild_id (str): The ID of the guild.
            name (str, optional): The name of the specific data to read (default: None).

        Returns:
            dict or any: If name is None, returns a dictionary of guild data.
                         If name is provided and the data exists, returns the value.
                         If name is provided and the data doesn't exist, returns None.
        """
        document = self.client["wolfie"]["guilds"]
        raw_data = document.find({"_id" : guild_id}, {})
        for data in raw_data:
            if name is not None:
                is_present = name in data
                if is_present is False:
                    return None
                return data[name]
        return raw_data

    def delete_guild_data(self, guild_id, name):
        """
        Deletes guild data with the specified name.

        Args:
            guild_id (str): The ID of the guild.
            name (str): The name of the data to delete.
        """
        document = self.client["wolfie"]["guilds"]
        document.update_one({"_id" : guild_id}, { "$unset" : { name : {} } })
