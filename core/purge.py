from discord.ext import commands
from discord.commands import slash_command
from classes.utils import Utils

class Purge(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.bot_utils = Utils()

    async def purge(self, ctx, amount = 1):
        if not await self.bot_utils.is_mod(ctx):
            return
        
        await ctx.channel.purge(limit=int(amount))
        await ctx.respond(str(amount) + " messages have been deleted!", delete_after=3)

def setup(bot):
    bot.add_cog(Purge(bot))