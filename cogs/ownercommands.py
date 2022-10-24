import discord

from discord.ext import commands, bridge
from discord.commands import slash_command
from discord import SlashCommandGroup
from database.database import GuildDatabase
from classes.utils import Utils

gd = GuildDatabase()
class OwnerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils()
        
    @bridge.bridge_group()
    async def owner(self, ctx: bridge.BridgeContext): pass

    @owner.command()
    async def set_admin(self, ctx, role: discord.Role):
        if await self.utils.is_owner(ctx) is not True:
            return
        
        gd.update_guild_key(ctx.guild.id, "admin_id", role.id)
        await self.utils.notify(ctx, "Admin set", f"Admin set to {role.mention}", "Owner commands")

def setup(bot):
    bot.add_cog(OwnerCommands(bot))
