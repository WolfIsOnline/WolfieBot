"""
Casino System
"""
# pylint: disable=no-name-in-module, import-error
from wolfiebot.database.database import Database

database = Database()

class Casino():
    """
    A class representing a casino.

    Provides methods for depositing, withdrawing, transferring funds,
    checking balance, and generating transaction IDs.
    """
    def deposit(self, user_id, amount : int):
        """
        Deposit the specified amount into the user's casino account.

        Args:
            user_id (int): The ID of the user.
            amount (int): The amount to be deposited.

        Returns:
            None
        """
        balance = self.get_balance(user_id)
        new_balance = balance + amount
        database.edit_user_data(user_id, "casino_balance", new_balance)

    def withdraw(self, user_id, amount : int) -> int:
        """
        Withdraw the specified amount from the user's casino account.

        Args:
            user_id (int): The ID of the user.
            amount (int): The amount to be withdrawn.

        Returns:
            int: The amount that was successfully withdrawn,
            or -1 if the withdrawal is not possible.

        """
        if self.is_sufficient(user_id, amount) is False:
            return -1
        balance = self.get_balance(user_id)
        new_balance = balance - amount
        database.edit_user_data(user_id, "casino_balance", new_balance)
        return amount

    def is_sufficient(self, user_id, amount : int) -> bool:
        """
        Check if the user's casino account has sufficient balance for a withdrawal.

        Args:
            user_id (int): The ID of the user.
            amount (int): The amount to be withdrawn.

        Returns:
            bool: True if the account has sufficient balance, False otherwise.

        """
        balance = self.get_balance(user_id)
        if balance >= amount:
            return True
        return False

    def get_balance(self, user_id) -> int:
        """
        Get the current balance in the user's casino account.

        Args:
            user_id (int): The ID of the user.

        Returns:
            int: The current balance in the casino account.

        """
        balance = database.read_user_data(user_id, "casino_balance")
        if balance is None:
            database.edit_user_data(user_id, "casino_balance", 0)
            balance = 0
        return balance
