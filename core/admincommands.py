import discord

from discord.ext import commands
from discord.commands import slash_command
from discord import SlashCommandGroup
from core.automove import AutoMove
from core.economy import Economy
from core.modlogs import ModLogs
from core.purge import Purge
from core.welcome import Welcome

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.automove = AutoMove(bot)
        self.economy = Economy(bot)
        self.modlogs = ModLogs(bot)
        self.purge = Purge(bot)
        self.welcome = Welcome(bot)

    admin = SlashCommandGroup("admin", "Admin commands")

    @admin.command(description="Test")
    async def test(self, ctx):
        await self.automove.test(ctx)

    @admin.command(description="Sets autoroom")
    async def setautoroom(self, ctx, id):
        await self.automove.setautoroom(ctx, id)

    @admin.command(description="Give's user money")
    async def givemoney(self, ctx, amount, user: discord.User):
        await self.economy.givemoney(ctx, amount, user)

    @admin.command(description="Take user money")
    async def takemoney(self, ctx, amount, user: discord.User):
        await self.economy.takemoney(ctx, amount, user)

    @admin.command(description="Set modlog to current channel")
    async def setmodlog(self, ctx):
        await self.modlogs.setmodlog(ctx)

    @admin.command(description="Deletes specified number of messages in channel.")
    async def purge(self, ctx, amount = 1):
        await self.purge.purge(ctx, amount)

    @admin.command(description="Sets welcome channel")
    async def setwelcome(self, ctx, id):
        await self.welcome.setwelcome(ctx, id)

    @admin.command()
    async def displaywelcome(self, ctx):
        await self.welcome.on_member_join(ctx.author)


def setup(bot):
    bot.add_cog(AdminCommands(bot))