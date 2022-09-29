from discord import slash_command
from discord.ext import commands
from database.database import Guild_DataBase

db = Guild_DataBase()

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @slash_command(description="")
    async def set_welcome(self, ctx):
        db.update_guild_key(ctx.guild.id, "welcome_channel", ctx.channel.id)
        await ctx.respond("Welcome channel set")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        pass

def setup(bot):
    bot.add_cog(Welcome(bot))