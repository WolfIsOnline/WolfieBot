import discord

from discord import slash_command
from discord.ext import commands
from database.database import Guild_DataBase
from classes.utils import Utils

db = Guild_DataBase()

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils()
    
    async def setwelcome(self, ctx, id):
        db.update_guild_key(ctx.guild.id, "welcome_channel", id)
        await ctx.respond("Welcome channel set")


    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild.name
        member_name = member.id
        welcome = discord.Embed(title=f"Welcome to {guild}", description=f"Hi <@{member_name}> \n\n• **I hope you enjoy your stay!**\n\n• **Check out the following channels.**\n\n <a:ng_bluearrowright:996149975471902760> Get your roles from <#983869250768883722>\n\n<a:ng_bluearrowright:996149975471902760> Current free games <#967074827108245554>\n\n<a:ng_bluearrowright:996149975471902760> Newest <#973745210016280577>", color=self.utils.DEFAULT_COLOR)
        welcome.set_author(name=guild, icon_url=member.guild.icon.url)
        welcome.set_thumbnail(url=member.display_avatar)
        welcome.set_image(url=member.guild.banner.url)
        channel = self.bot.get_channel(int(db.get_guild_key(member.guild.id, "welcome_channel")))
        await channel.send(embed=welcome)

def setup(bot):
    bot.add_cog(Welcome(bot))