import discord
import logging

from pydoc import describe
from discord.ext import commands, bridge
from discord.commands import slash_command
from discord.utils import get
from discord import SlashCommandGroup
from classes.utils import Utils
from database.database import Guild_DataBase

gd = Guild_DataBase()
class Dev(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.bot_util = Utils()
    
    @slash_command(description="Check if owner")
    async def check_owner(self, ctx):
        if await self.bot_util.is_owner(ctx):
            return await ctx.respond("You are the owner")

    @slash_command(description="Set admin role")
    async def set_admin(self, ctx, id):
        if not await self.bot_util.is_owner(ctx):
            return
        
        gd.update_guild_key(ctx.guild.id, "admin_id", id)
        await self.bot_util.notify(ctx, f"Admin set to <@&{id}>")

    @slash_command(description="Set mod role")
    async def set_mod(self, ctx, id):
        if not await self.bot_util.is_owner(ctx):
            return
        gd.update_guild_key(ctx.guild.id, "mod_id", id)
        await self.bot_util.notify(ctx, f"Mod set to <@&{id}>")

    @slash_command(description="check")
    async def notify_embed(self, ctx):
        if not await self.bot_util.is_owner(ctx):
            return
        await self.bot_util.notify(ctx, "test")

    @slash_command(description="reloads cog")
    async def reload(self, ctx, cog):
        if not await self.bot_util.is_owner(ctx):
            return

        self.bot.reload_extension(f"core.{cog}")
        await self.bot_util.notify(ctx, f"{cog} successfully reloaded")

    @slash_command(description="load cog")
    async def load(self, ctx, cog):
        if not await self.bot_util.is_owner(ctx):
            return
        self.bot.load_extension(f"core.{cog}")
        await self.bot_util.notify(ctx, f"{cog} successfully loaded")

    @slash_command(description="unload cog")
    async def unload(self, ctx, cog):
        if not await self.bot_util.is_owner(ctx):
            return
        self.bot.unload_extension(f"core.{cog}")
        await self.bot_util.notify(ctx, f"{cog} successfully unloaded")

        
def setup(bot):
    bot.add_cog(Dev(bot))