from discord.ext import commands
from discord.commands import slash_command
from utils import Utils

class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    bot_util = Utils()
    @slash_command(description="is_connected(self, ctx)")
    async def check_connection(self, ctx):
        if(await self.bot_util.is_connected(ctx)):
            return await ctx.respond("i'm connected")
        return await ctx.respond("i'm not connected")

def setup(bot):
    bot.add_cog(Dev(bot))