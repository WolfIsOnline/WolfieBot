import discord

from discord.ext import commands, bridge
from discord.commands import slash_command
from classes.transactions import Transactions
from classes.utils import Utils
from database.database import UserDatabase

CURRENCY_NAME = "Eurodollar"
CURRENCY_ABBR = "ecu"
CURRENCY_SYMBOL = "§"
BANKING_ICON = "https://i.imgur.com/pDzfl95.gif"
ud = UserDatabase()


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils()
        self.transactions = Transactions()

    async def payday(self, ctx, amount : int):
        await self.transactions.deposit(ctx.author.id, amount, "payday", "nocturnia")

    async def give_money(self, ctx, amount, user: discord.User):
        await self.transactions.deposit(user.id, amount, f"dev deposit", "noctornia_bank")

    async def take_money(self, ctx, amount, user: discord.User):
        await self.transactions.withdraw(user.id, amount, f"dev withdrew", ctx.author.name)
        
    async def transfer(self, ctx, amount, transferer, transferee):
        
        sufficient = await self.transactions.sufficient_funds(transferer.id, amount)
        if sufficient is False:
            return await self.utils.notify(ctx, "Insufficient Funds", f"transfer was declined", "Bank")
        
        transferer_name = ctx.author.guild.get_member(transferer.id)
        transferee_name = ctx.author.guild.get_member(transferee.id)
        await self.transactions.withdraw(transferer.id, amount, f"transfer to {transferee}", "")
        await self.transactions.deposit(transferee.id, amount, f"transfer from {transferer}", "")
        await ctx.respond(f"{ctx.author.mention} transfered **{CURRENCY_SYMBOL}{amount}** to {transferee.mention}")
        
    async def balance(self, ctx, dm: bool = False):
        try:
            balance = int(ud.get_user_key(ctx.author.id, "bank_balance"))
        except:
            balance = 0
        embed = discord.Embed(title="Nocturnia Bank", description=f"Available Balance: **{CURRENCY_SYMBOL}{balance:,}**", color=self.utils.DEFAULT_COLOR)
        embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
        embed.set_thumbnail(url=ctx.author.display_avatar)
        transactions = ud.get_transaction(ctx.author.id)
        if transactions is not None:
            transactions.reverse()
            display = 0
            sign = ""
            for c in transactions:
                display += 1
                if display > 5:
                    break
                if c["type"] == "incoming":
                    sign = "+"
                elif c["type"] == "outgoing":
                    sign = "-"
                amount = int(c["amount"])
                reason = c["reason"]
                embed.add_field(name=c["date"],
                                value=f"```{reason}\t\t\t\t\t\t\t\t\t{sign}{CURRENCY_SYMBOL}{amount:,}```",
                                inline=False)
        else:
            embed.add_field(name=f"No recent transactions", value="Recent transactions will show up here", inline=False)
        if dm is False:
            await ctx.respond(embed=embed)
        elif dm is True:
            try:
                await ctx.author.send(embed=embed)
            except:
                await ctx.respond("I cannot send you a message. You have DMS disabled or you have blocked me")
            await ctx.respond("Balance sent in DM")


def setup(bot):
    bot.add_cog(Economy(bot))
