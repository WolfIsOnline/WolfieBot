from doctest import debug_script
from email import message
import discord
from discord.ext import commands
from discord.commands import slash_command
from pyparsing import empty
from database.guild_db import Guild_DataBase

class ModLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Set modlog to current channel")
    async def set_modlog(self, ctx):
        db = Guild_DataBase()
        guild_id = ctx.guild.id
        channel_id = ctx.channel.id
        db.update_guild_key(guild_id, "modlog_channel", channel_id)
        await ctx.respond("Channel set")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        await self.send_msglog(message, "Message was deleted", 0xffa500)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot:
            return
        await self.send_msglog(before, "Message was edited", 0x738adb, after.content)

    @commands.Cog.listener()
    async def on_member_join(member):
        pass

    async def send_msglog(self, message, action, color, after = None):
        log_embed = discord.Embed(title=action, description=message.content, color=color)
        log_embed.set_author(name=message.author, icon_url=message.author.avatar.url)
        if after != None:
            log_embed.add_field(name="After edit", value=str(after), inline=False)
        log_embed.add_field(name=f"Message author:", value=message.author, inline=True)
        log_embed.add_field(name=f"Channel: ", value=message.channel.mention, inline=True)
        log_embed.set_footer(text=f"ID: {message.id}")

        db = Guild_DataBase()
        channel = db.get_guild_key(message.guild.id, "modlog_channel")
        await self.bot.get_channel(int(channel)).send(embed=log_embed)

def setup(bot):
    bot.add_cog(ModLogs(bot))

