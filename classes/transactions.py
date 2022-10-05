from database.database import UserDatabase

ud = UserDatabase()
class Transactions():

    def get_balance(self, user_id):
        balance = ud.get_user_key(user_id, "bank_balance")
        if(balance == "None"):
            balance = 0
        return int(balance)
        
    async def insufficient_funds(self, user_id, amount):
        if self.get_balance(user_id) < amount:
            return True
        return False

    async def deposit(self, user_id, amount, reason, member):
        try:
            camount = int(ud.get_user_key(user_id, "bank_balance"))
        except:
            camount = 0
        
        _amount = camount + int(amount)
        ud.update_user_key(user_id, "bank_balance", _amount)
        ud.add_transaction(user_id, amount, reason, "incoming", member)
        return _amount

    async def withdraw(self, user_id, amount, reason, member):
        try:
            camount = int(ud.get_user_key(user_id, "bank_balance"))
        except:
            camount = 0
        _amount = camount - int(amount)
        ud.update_user_key(user_id, "bank_balance", _amount)
        ud.add_transaction(user_id, amount, reason, "outgoing", member)
        return _amount
