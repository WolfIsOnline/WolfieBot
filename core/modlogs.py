from email import message
import discord
from discord.ext import commands
from discord.commands import slash_command
from pyparsing import empty

class ModLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
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
        prev_invites = invites[member.guild.id]
        pass

    async def send_msglog(self, message, action, color, after = None):
        log_embed = discord.Embed(title=action, description=message.content, color=color)
        log_embed.set_author(name=message.author, icon_url=message.author.avatar.url)
        if action != None:
            log_embed.add_field(name="After edit", value=str(after), inline=False)
        log_embed.add_field(name=f"Message author:", value=message.author, inline=True)
        log_embed.add_field(name=f"Channel: ", value=message.channel.mention, inline=True)
        log_embed.set_footer(text=f"ID: {message.id}")        
        await self.bot.get_channel(int(1022075613957333045)).send(embed=log_embed)

def setup(bot):
    bot.add_cog(ModLogs(bot))

