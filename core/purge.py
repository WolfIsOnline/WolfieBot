import asyncio
from discord import message_command
from discord.ext import commands
from discord.commands import slash_command

class Purge(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Deletes specified number of messages in channel.")
    async def purge(self, ctx, amount = 1):
        await ctx.channel.purge(limit=int(amount))
        await ctx.respond(str(amount) + " messages have been deleted!", delete_after=3)


def setup(bot):
    bot.add_cog(Purge(bot))