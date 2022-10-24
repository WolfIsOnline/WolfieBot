import discord

from discord.ext import commands, bridge
from discord.commands import slash_command
from discord import SlashCommandGroup
from classes.utils import Utils
from cogs.nocturnia import Nocturnia
from cogs.economy import Economy


currency_name = "Eurodollar"
currency_abbr = "ecu"
currency_symbol = "§"

class UserCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils()
        self.nocturnia = Nocturnia(bot)
        self.economy = Economy(bot)
    
    # GENERAL COMMANDS
    @bridge.bridge_command(description="Get users profile picture")
    async def pfp(self, ctx, user: discord.User):
        avatar = discord.Embed(color=self.utils.DEFAULT_COLOR)
        avatar.set_image(url=user.display_avatar)
        await ctx.respond(embed=avatar)

    @bridge.bridge_command(description="Pong")
    async def ping(self, ctx):
        await ctx.respond("Pong")
    
    #ECONOMY COMMANDS
    @bridge.bridge_command(description="Transfer funds to another member")
    async def transfer(self, ctx, amount : int, user: discord.User):
        await self.economy.transfer(ctx, amount, ctx.author, user)
        
    @bridge.bridge_command(description="Get paid every hour")
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def payday(self, ctx):
        amount = 1000
        await self.economy.payday(ctx, amount)
        await self.utils.notify(ctx, "Deposit", f"**{currency_symbol}{amount:,}** has been deposited into your account", "Nocturnia Bank", self.bot.user.display_avatar)
        
    @bridge.bridge_command(description="Show current balance")
    async def balance(self, ctx, dm: bool = False):
        await self.economy.balance(ctx, dm)
        


def setup(bot):
    bot.add_cog(UserCommands(bot))
