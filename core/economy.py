import discord

from discord.ext import commands
from discord.commands import slash_command
from classes.transactions import Transactions
from classes.utils import Utils
from database.database import UserDatabase

currency_name = "Eurodollar"
currency_abbr = "ecu"
currency_symbol = "§"
ud = UserDatabase()


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

    async def give_money(self, ctx, amount, user: discord.User):
        await self.transactions.deposit(user.id, amount, f"admin deposit", "noctornia_bank")

    async def take_money(self, ctx, amount, user: discord.User):
        await self.transactions.withdraw(user.id, amount, f"admin withdrew", ctx.author.name)
        
    async def transfer(self, ctx, amount, transferer, transferee):
        
        sufficient = await self.transactions.sufficient_funds(transferer.id, amount)
        if sufficient is False:
            return await self.utils.notify(ctx, "Insufficient Funds", f"transfer was declined", "Bank")
        
        transferer_name = ctx.author.guild.get_member(transferer.id)
        transferee_name = ctx.author.guild.get_member(transferee.id)
        await self.transactions.withdraw(transferer.id, amount, f"transfer to {transferee}", "")
        await self.transactions.deposit(transferee.id, amount, f"transfer from {transferer}", "")
        await ctx.respond(f"{ctx.author.mention} transfered **{currency_symbol}{amount}** to {transferee.mention}")
        
        
            

    @slash_command(description="Show current balance")
    async def balance(self, ctx, dm: bool = False):
        try:
            balance = int(ud.get_user_key(ctx.author.id, "bank_balance"))
        except:
            balance = 0
        embed = discord.Embed(title="Nocturnia Bank", description=f"Available Balance: {currency_symbol}{balance:,}", color=self.utils.DEFAULT_COLOR)
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
                                value=f"```{reason}\t\t\t\t\t\t\t\t\t{sign}{currency_symbol}{amount:,} ```",
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
