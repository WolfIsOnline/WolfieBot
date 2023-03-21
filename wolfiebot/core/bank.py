import logging
import uuid
import datetime

from wolfiebot.database.database import Database

db = Database()
log = logging.getLogger(__name__)

class Bank:
    def deposit(self, user_id, amount : int, statement : str):
        balance = self.get_balance(user_id)
        new_balance = balance + amount
        
        transaction_id = self.get_id()
        data = {"id": transaction_id, "amount" : amount, "date" : datetime.datetime.now(), "type" : "deposit", "statement" : statement}
        
        db.append_user_data(user_id, "transactions", data)
        db.edit_user_data(user_id, "balance", new_balance)
        log.debug(f"transaction {transaction_id} complete")
        
    def withdraw(self, user_id, amount : int, statement : str) -> int:
        if self.is_sufficient(user_id, amount) is False:
            return -1
        balance = self.get_balance(user_id)
        new_balance = balance - amount
        
        transaction_id = self.get_id()
        data = {"id": transaction_id,"amount" : amount, "date" : datetime.datetime.now(), "type" : "withdraw", "statement" : statement}
        
        db.append_user_data(user_id, "transactions", data)
        db.edit_user_data(user_id, "balance", new_balance)
        log.debug(f"transaction {transaction_id} complete")
        return amount
        
    def transfer(self, sender_id, receiver_id, amount : int, sender_statment, receiver_statment) -> int:
        
        confirmed_amount = self.withdraw(sender_id, amount, sender_statment)
        if confirmed_amount <= -1:
            return -1
        self.deposit(receiver_id, confirmed_amount, receiver_statment)
        return confirmed_amount
        
    def is_sufficient(self, user_id, amount : int) -> bool:
        balance = self.get_balance(user_id)
        if balance >= amount:
            return True
        return False
        
    def get_balance(self, user_id) -> int:
        balance = db.read_user_data(user_id, "balance")
        if balance is None:
            db.edit_user_data(user_id, "balance", 0)
            balance = 0
        return balance
    
    def get_id(self) -> str:
        return uuid.uuid4().hex
