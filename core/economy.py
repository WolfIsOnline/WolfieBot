import discord

from discord.ext import commands
from discord.commands import slash_command
from classes.transactions import Transactions
from classes.utils import Utils
from datetime import datetime
from database.database import _User_Database

currency_name = "Eurodollar"
currency_abbr = "ecu"
currency_symbol = "§"
ud = _User_Database()

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils()
        self.transactions = Transactions()

    @slash_command(description="Get paid every hour")
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def payday(self, ctx):
        amount = 1000
        await self.transactions.deposit(ctx.author.id, amount, "payday", "wolfiebot")
        await self.utils.notify(ctx, "Deposit", f"**{currency_symbol}{amount:,}** has been deposited into your account", "Nocturnia Bank", ctx.guild.icon.url)

    async def givemoney(self, ctx, amount, user: discord.User):
        id = user.id
        _amount = await self.transactions.deposit(id, amount, f"admin deposit", "noctornia_bank")

    async def takemoney(self, ctx, amount, user: discord.User):
        id = user.id
        _amount = await self.transactions.withdraw(id, amount, f"admin withdrew", ctx.author.name)  

    @slash_command(description="Show current balance")
    async def balance(self, ctx, dm : bool = False):
        try:
            balance = int(ud.get_user_key(ctx.author.id, "bank_balance"))
        except:
            balance = 0
        embed = discord.Embed(title="Nocturnia Bank", description=f"Available Balance: {currency_symbol}{balance:,}", color=self.utils.DEFAULT_COLOR)
        embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
        embed.set_thumbnail(url=ctx.author.display_avatar)
        transactions = ud.get_transaction(ctx.author.id)
        if not transactions == None:
            transactions.reverse()
            display = 0
            amount = 0
            sign = ""
            for c in transactions:
                display += 1
                if display > 5:
                    break
                if c["type"] == "incoming":
                    sign = "+"
                  #  amount = "+ " + currency_symbol + c["amount"]
                elif c["type"] == "outgoing":
                    sign = "-"
                   # amount = "- " + currency_symbol + c["amount"]
                amount = int(c["amount"])
                reason = c["reason"]
                embed.add_field(name=c["date"], value=f"```{reason}\t\t\t\t\t\t\t\t\t{sign}{currency_symbol}{amount:,} ```", inline=False)
                #embed.add_field(name=c["date"], value="```" + c["reason"] + "\t\t\t\t\t\t\t\t\t" + amount + "```", inline=False)
        else:
            embed.add_field(name=f"No recent transactions", value="Recent transactions will show up here", inline=False)
        if dm == False:
            await ctx.respond(embed=embed)
        elif dm == True:
            try:
                await ctx.author.send(embed=embed)
            except: await ctx.respond("I cannot send you a message. You have DMS disabled or you have blocked me")
            await ctx.respond("Balance sent in DM")

def setup(bot):
    bot.add_cog(Economy(bot))
    #kd
