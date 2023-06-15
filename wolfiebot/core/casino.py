from wolfiebot.database.database import Database

database = Database()

class Casino():
    
    def deposit(self, user_id, amount : int):
        balance = self.get_balance(user_id)
        new_balance = balance + amount
        database.edit_user_data(user_id, "casino_balance", new_balance)
        
    def withdraw(self, user_id, amount : int) -> int:
        if self.is_sufficient(user_id, amount) is False:
            return -1
        balance = self.get_balance(user_id)
        new_balance = balance - amount
        database.edit_user_data(user_id, "casino_balance", new_balance)
        return amount
    
    def is_sufficient(self, user_id, amount : int) -> bool:
        balance = self.get_balance(user_id)
        if balance >= amount:
            return True
        return False 
        
    def get_balance(self, user_id) -> int:
        balance = database.read_user_data(user_id, "casino_balance")
        if balance is None:
            database.edit_user_data(user_id, "casino_balance", 0)
            balance = 0
        return balance