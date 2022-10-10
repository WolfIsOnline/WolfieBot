import discord
import pytz

from discord.ext import commands
from database.database import GuildDatabase
from discord.ui import Button, View
from classes.utils import Utils

db = GuildDatabase()


class ModLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils()

    async def unban(self, ctx, user_id):
        user = await self.bot.fetch_user(user_id)
        await ctx.guild.unban(user)

    async def ban(self, member, reason=None):
        await member.ban(reason=reason)

    async def set_mod_log(self, ctx, channel_id):
        guild_id = ctx.guild.id
        db.update_guild_key(guild_id, "modlog_channel", channel_id)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        ban_log = await guild.audit_logs(limit=1, action=discord.AuditLogAction.ban).flatten()
        embed = discord.Embed(title="User Banned", color=0xb33a3a)
        embed.add_field(name="User", value=user, inline=True)
        embed.add_field(name="Moderator", value=ban_log[0].user, inline=True)
        embed.add_field(name="Reason", value=ban_log[0].reason, inline=False)
        embed.set_footer(text=f"Account ID: {user.id}")

        channel = db.get_guild_key(guild.id, "modlog_channel")

        button = Button(label="Unban", style=discord.ButtonStyle.green)

        async def button_callback(interaction):
            await self.unban(user, user.id)
            button.disabled = True
            button.label = "User Unbanned"
            view = View()
            view.add_item(button)
            await interaction.response.edit_message(view=view)

        button.callback = button_callback
        view = View()
        view.add_item(button)
        await self.bot.get_channel(channel).send(embed=embed, view=view)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        unban_log = await guild.audit_logs(limit=1, action=discord.AuditLogAction.unban).flatten()
        embed = discord.Embed(title="User Unbanned", color=0x2d7d46)
        embed.add_field(name="User", value=user, inline=True)
        embed.add_field(name="Moderator", value=unban_log[0].user, inline=True)
        embed.add_field(name="Reason", value=unban_log[0].reason, inline=False)
        embed.set_footer(text=f"Account ID: {user.id}")

        channel = db.get_guild_key(guild.id, "modlog_channel")
        await self.bot.get_channel(channel).send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        await self.send_msg_log(message, "Message was deleted", 0xffa500)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if not before.nick == after.nick:
            entry = await before.guild.audit_logs(limit=1, action=discord.AuditLogAction.member_update).flatten()
            embed = discord.Embed(title="Nickname Changed", description=before.nick, color=0x738adb)
            embed.add_field(name="After change", value=after.nick, inline=True)
            embed.add_field(name="Changed by", value=entry[0].user, inline=True)
            embed.set_author(name=after, icon_url=after.display_avatar)
            embed.set_footer(text=f"Account ID: {after.id}")

            channel = int(db.get_guild_key(before.guild.id, "modlog_channel"))
            await self.bot.get_channel(channel).send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot:
            return
        await self.send_msg_log(before, "Message was edited", 0x738adb, after.content)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            await member.guild.fetch_ban(member)
            return
        except discord.NotFound:
            pass
        embed = discord.Embed(title="User Left", description=f"{member} has left the server", color=0xffffff)
        embed.set_author(name=f"{member}", icon_url=member.display_avatar)
        embed.set_footer(text=f"Account ID: {member.id}")
        channel = db.get_guild_key(member.guild.id, "modlog_channel")

        await self.bot.get_channel(int(channel)).send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(title="User Joined", description=f"{member.mention} joined the server", color=0x2d7d46)
        embed.set_author(name=f"{member}", icon_url=member.display_avatar)
        embed.add_field(name=f"Account created",
                        value=member.created_at.astimezone(pytz.timezone("US/Eastern")).strftime("%c"))
        embed.set_footer(text=f"Account ID: {member.id}")

        channel = db.get_guild_key(member.guild.id, "modlog_channel")
        await self.bot.get_channel(int(channel)).send(embed=embed)

    async def send_msg_log(self, message, action, color, after=None):
        log_embed = discord.Embed(title=action, description=message.content, color=color)
        log_embed.set_author(name=message.author, icon_url=message.author.display_avatar)
        if after is not None:
            log_embed.add_field(name="After edit", value=str(after), inline=False)
        log_embed.add_field(name=f"Message author:", value=message.author, inline=True)
        log_embed.add_field(name=f"Channel: ", value=message.channel.mention, inline=True)
        log_embed.set_footer(text=f"ID: {message.id}")

        channel = db.get_guild_key(message.guild.id, "modlog_channel")
        await self.bot.get_channel(int(channel)).send(embed=log_embed)

    async def send_error_msg(self, guild, message, error_info, error_code):
        guild_id = guild.id
        bot = guild.get_member(self.bot.user.id)
        error = discord.Embed(description=message, title=error_info, color=0xb33a3a)
        error.set_author(name=error_code)
        error.set_thumbnail(url=bot.display_avatar)
        channel = db.get_guild_key(guild_id, "modlog_channel")
        await self.bot.get_channel(int(channel)).send(embed=error)
        
def setup(bot):
    bot.add_cog(ModLogs(bot))
