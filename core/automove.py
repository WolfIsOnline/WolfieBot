import discord

from unicodedata import category

from discord.ext import commands
from database.database import GuildDatabase

db = GuildDatabase()


class AutoMove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def check_empty(self, member, before_id):
        check_id = db.get_guild_key(member.guild.id, f"automove_{before_id}")

        if not str(before_id) == check_id:
            return

        channel = self.bot.get_channel(before_id)
        if len(channel.members) == 0:
            await channel.delete(reason="channel is empty")
            db.delete_guild_key(member.guild.id, f"automove_{before_id}", before_id)

    async def set_auto_room(self, ctx, channel_id):
        guild_id = ctx.guild.id
        db.update_guild_key(guild_id, "automove_source", channel_id)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel:
            old_id = before.channel.id
            await self.check_empty(member, old_id)
        if after.channel:
            auto_id = db.get_guild_key(member.guild.id, "automove_source")
            new_id = after.channel.id
            if str(new_id) == str(auto_id):
                source_channel = self.bot.get_channel(int(auto_id))
                channel = await member.guild.create_voice_channel(
                    member.name,
                    reason="user requested",
                    category=source_channel.category,
                    bitrate=source_channel.bitrate,
                    user_limit=source_channel.user_limit,
                    overwrites={
                        member: discord.PermissionOverwrite(view_channel=True, connect=True, speak=True,
                                                            manage_channels=True, manage_permissions=True, mute_members=True, deafen_members=True)
                    })
                await member.move_to(channel)
                db.add_guild_key(member.guild.id, f"automove_{channel.id}", channel.id)


def setup(bot):
    bot.add_cog(AutoMove(bot))
