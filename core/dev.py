import discord
import logging

from pydoc import describe
from discord.ext import commands, bridge
from discord.commands import slash_command
from discord.utils import get
from discord import SlashCommandGroup
from classes.utils import Utils
from database.database import Guild_DataBase
from core.quotes import Quotes

gd = Guild_DataBase()
class Dev(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils()
        self.quotes = Quotes(bot)

    dev = SlashCommandGroup("dev", "Dev commands", checks=[commands.is_owner().predicate])

    @dev.command(description="Test")
    async def test(self, ctx):
        await ctx.respond("working!")

    @dev.command(description="Set admin role")
    async def setadmin(self, ctx, id):
        gd.update_guild_key(ctx.guild.id, "admin_id", id)
        await self.utils.notify(ctx, "Admin set", f"Admin set to <@&{id}>", "Dev commands")

    @dev.command(description="Set mod role")
    async def setmod(self, ctx, id):
        gd.update_guild_key(ctx.guild.id, "mod_id", id)
        await self.utils.notify(ctx, "Mod set", f"Mod set to <@&{id}>", "Dev commands")


    @dev.command(description="reload cog")
    async def reload(self, ctx, cog):
        self.bot.reload_extension(f"core.{cog}")
        await self.utils.notify(ctx, "Reloaded", f"{cog} successfully reloaded", "Dev commands")

    @dev.command(description="load cog")
    async def load(self, ctx, cog):
        self.bot.load_extension(f"core.{cog}")
        await self.utils.notify(ctx, "Loaded", f"{cog} successfully loaded", "Dev commands")

    @dev.command(description="unload cog")
    async def unload(self, ctx, cog):
        self.bot.unload_extension(f"core.{cog}")
        await self.utils.notify(ctx, "Unloaded", f"{cog} successfully unloaded", "Dev commands")

    @dev.command(description="Update quote file")
    async def forceupdate(self, ctx):
        await self.quotes.force_refresh()
        await self.utils.notify(ctx, "Updated", "Log file updated", "Dev commands")

        
def setup(bot):
    bot.add_cog(Dev(bot))