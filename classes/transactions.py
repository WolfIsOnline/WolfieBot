from database.database import _User_Database

ud = _User_Database()
class Transactions():

    async def insufficient_funds(self, user_id, amount):
        balance = int(ud.get_user_key(user_id, "bank_balance"))
        if balance < amount:
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