import discord

from discord.ext import commands
from discord.commands import slash_command
from discord import SlashCommandGroup
from core.automove import AutoMove
from core.economy import Economy
from core.modlogs import ModLogs
from core.welcome import Welcome
from core.economy import Economy
from core.quotes import Quotes
from classes.utils import Utils

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.automove = AutoMove(bot)
        self.modlogs = ModLogs(bot)
        self.welcome = Welcome(bot)
        self.quotes = Quotes(bot)
        self.economy = Economy(bot)
        self.utils = Utils()

    admin = SlashCommandGroup("admin", "Admin commands")

    @admin.command(description="Sets autoroom")
    async def setautoroom(self, ctx, id):
        await self.automove.setautoroom(ctx, id)

    @admin.command(description="Give's user money")
    async def givemoney(self, ctx, amount : int, user: discord.User):
        await self.economy.givemoney(ctx, amount, user)
        await self.utils.notify(ctx, "Money Given", f"§{amount:,} has been given to {user}", "Admin commands")

    @admin.command(description="Take user money")
    async def takemoney(self, ctx, amount : int, user: discord.User):
        await self.economy.takemoney(ctx, amount, user)
        await self.utils.notify(ctx, "Money Taken", f"§{amount:,} has been taken from {user}", "Admin commands")

    @admin.command(description="Set modlog to specified channel")
    async def setmodlog(self, ctx, id):
        await self.modlogs.setmodlog(ctx, id)
        await self.utils.notify(ctx, "Mod logs set", f"mod logs will go to <#{id}>", "Admin commands")

    @admin.command(description="Sets welcome channel")
    async def setwelcome(self, ctx, id):
        await self.welcome.setwelcome(ctx, id)

    @admin.command(description="Update quote file")
    async def forceupdate(self, ctx):
        await self.quotes.force_refresh()
        await ctx.respond("Log file updated")

    @admin.command(description="Set quotes channel")
    async def setquotes(self, ctx, id):
        await self.quotes.setquotes(id)
        await ctx.respond("Quotes channel set")
        
def setup(bot):
    bot.add_cog(AdminCommands(bot))
