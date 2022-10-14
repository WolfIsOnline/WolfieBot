import discord
import asyncio

from discord.ext import commands
from database.database import GuildDatabase
from discord.commands import slash_command

from core.modlogs import ModLogs

gd = GuildDatabase()
KEY_ID = "autoroles"

class AutoRole(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.mod_logs = ModLogs(bot)
        
    @commands.Cog.listener()
    async def on_member_join(self, member):
        role_ids = gd.get_guild_key_array(member.guild.id, KEY_ID)
        for role_id in role_ids:
            role = member.guild.get_role(role_id)
            try:
                await member.add_roles(role, reason="user joined")
            except discord.Forbidden as e:
                    await self.mod_logs.send_error_msg(member.guild, f"could not apply {role.mention} to {member.mention}", e.text, f"Error {e.code}")
            await asyncio.sleep(1) # need to throttle adding each user or mod logs will go crazy
                            
    async def add_auto_role(self, role: discord.Role):
        gd.append_guild_key_array(role.guild.id, KEY_ID, role.id)

def setup(bot):
    bot.add_cog(AutoRole(bot))