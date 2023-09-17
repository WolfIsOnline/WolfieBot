"""
Banking System
"""
import logging
import uuid
import datetime

# pylint: disable=no-name-in-module, import-error
from wolfiebot.database.database import Database

database = Database()
log = logging.getLogger(__name__)

class Bank:
    """
    A class representing a bank.

    Provides methods for depositing, withdrawing, transferring funds,
    checking balance, and generating transaction IDs.
    """
    def deposit(self, user_id, amount : int, statement : str):
        """
        Deposit funds into the user's account and record the transaction.

        Args:
            user_id (Any): The ID of the user.
            amount (int): The amount to deposit.
            statement (str): A statement describing the deposit transaction.

        Returns:
            None
        """
        balance = self.get_balance(user_id)
        new_balance = balance + amount

        transaction_id = self.get_id()
        data = {
            "id": transaction_id,
            "amount" : amount,
            "date" : datetime.datetime.now(),
            "type" : "deposit",
            "statement" : statement
        }

        database.append_user_data(user_id, "transactions", data)
        database.edit_user_data(user_id, "balance", new_balance)

    def withdraw(self, user_id, amount : int, statement : str) -> int:
        """
        Withdraw funds from the user's account and record the transaction.

        Args:
            user_id (Any): The ID of the user.
            amount (int): The amount to withdraw.
            statement (str): A statement describing the withdrawal transaction.

        Returns:
            int: The withdrawn amount if the withdrawal is successful, otherwise -1.
        """
        if self.is_sufficient(user_id, amount) is False:
            return -1
        balance = self.get_balance(user_id)
        new_balance = balance - amount

        transaction_id = self.get_id()
        data = {
            "id": transaction_id,
            "amount": amount,
            "date": datetime.datetime.now(),
            "type": "withdraw",
            "statement": statement
        }
        database.append_user_data(user_id, "transactions", data)
        database.edit_user_data(user_id, "balance", new_balance)
        return amount

    def transfer(
        self,
        sender_id,
        receiver_id,
        amount : int,
        sender_statment,
        receiver_statment
    ) -> int:
        """
        Transfer funds from one user's account to another and record the transactions.

        Args:
            sender_id (Any): The ID of the sender.
            receiver_id (Any): The ID of the receiver.
            amount (int): The amount to transfer.
            sender_statement (str): A statement from the sender's perspective.
            receiver_statement (str): A statement from the receiver's perspective.

        Returns:
            int: The transferred amount if the transfer is successful, otherwise -1.
        """
        confirmed_amount = self.withdraw(sender_id, amount, sender_statment)
        if confirmed_amount <= -1:
            return -1
        self.deposit(receiver_id, confirmed_amount, receiver_statment)
        return confirmed_amount

    def is_sufficient(self, user_id, amount : int) -> bool:
        """
        Check if the user has sufficient balance to perform a withdrawal.

        Args:
            user_id (Any): The ID of the user.
            amount (int): The amount to withdraw.

        Returns:
            bool: True if the user has sufficient balance, False otherwise.
        """
        balance = self.get_balance(user_id)
        if balance >= amount:
            return True
        return False

    def get_balance(self, user_id) -> int:
        """
        Get the balance of the user.

        Args:
            user_id (Any): The ID of the user.

        Returns:
            int: The balance of the user.
        """
        balance = database.read_user_data(user_id, "balance")
        if balance is None:
            database.edit_user_data(user_id, "balance", 0)
            balance = 0
        return balance

    def get_id(self) -> str:
        """
        Generate a unique transaction ID.

        Returns:
            str: A unique transaction ID.
        """
        return uuid.uuid4().hex
