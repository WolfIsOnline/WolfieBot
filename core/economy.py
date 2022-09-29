import discord

from discord.ext import commands
from discord.commands import slash_command
from database.database import User_Database
from classes.utils import Utils
from datetime import datetime

ud = User_Database()
currency_name = "Eurodollar"
currency_abbr = "ecu"
currency_symbol = "§"
class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils()

    @slash_command(description="Get paid every hour")
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def payday(self, ctx):
        amount = 1000
        await self.deposit(ctx.author.id, amount, "payday", "wolfiebot")
        await ctx.respond(f"{amount} has been deposited into your account. /balance to check your current balance")

    async def givemoney(self, ctx, amount, user: discord.User):
        if not await self.utils.is_owner(ctx):
            return

        id = user.id
        _amount = await self.deposit(id, amount, f"admin deposit", "noctornia_bank")
        await self.utils.notify(ctx, f"{amount} {currency_name}'s has been given to you.")

    async def takemoney(self, ctx, amount, user: discord.User):
        if not await self.utils.is_owner(ctx):
            return

        id = user.id
        _amount = await self.withdraw(id, amount, f"admin withdrew", ctx.author.name)
        await self.utils.notify(ctx, f"{amount} {currency_name}'s has been taken from you.")        


    @slash_command(description="Show current balance")
    async def balance(self, ctx, max_show: int = 5):
        try:
            balance = int(ud.get_user_key(ctx.author.id, "bank_balance"))
        except:
            balance = 0
        number = 0
        embed = discord.Embed(title="Nocturnia Bank", description=f"Available Balance: {currency_symbol}{balance:,}", color=self.utils.DEFAULT_COLOR)
        embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
        transactions = ud.get_transaction(ctx.author.id)
        if not transactions == None:
            transactions.reverse()
            display = 0
            for c in transactions:
                display += 1
                if display > max_show:
                    break
                if c["type"] == "incoming":
                    amount = "+ " + currency_symbol + c["amount"]
                elif c["type"] == "outgoing":
                    amount = "- " + currency_symbol + c["amount"]
                embed.add_field(name=c["date"], value="```" + c["reason"] + "\t\t\t\t\t\t\t\t" + amount + "```", inline=False)
        else:
            embed.add_field(name=f"No recent transactions", value="Recent transactions will show up here", inline=False)
        await ctx.respond(embed=embed)

    async def insufficient_funds(self, user_id):
        balance = int(ud.get_user_key(user_id, "bank_balance"))
        if balance < 0:
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

def setup(bot):
    bot.add_cog(Economy(bot))