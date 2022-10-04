import discord

from discord.ext import commands
from discord.commands import slash_command
from classes.transactions import Transactions

class Nocturnia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.transactions = Transactions()

    async def notify_death(self, user_id):
        balance = self.transactions.get_balance(user_id)
        await self.transactions.withdraw(user_id, balance, "donation to Nocturnia", "nocturnia")

        user = await self.bot.fetch_user(int(user_id))
        try: await user.send(f"You have died. Upon death, citzens are required to donate all assets to the Nocturnia Government. We want to thank you for your monetary contribution of **{balance:,} Eurodollar's** and these funds will be used responsibly to help serve the Nocturnia people. You are a true patriot.")
        except: pass

def setup(bot):
    bot.add_cog(Nocturnia(bot))