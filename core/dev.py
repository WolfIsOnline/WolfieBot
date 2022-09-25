import discord

from pydoc import describe
from discord.ext import commands
from discord.commands import slash_command
from classes.utils import Utils

utils = Utils()

class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="is_connected(self, ctx)")
    async def check_connection(self, ctx):
        if(await utils.is_connected(ctx)):
            return await ctx.respond("i'm connected")
        return await ctx.respond("i'm not connected")

    @slash_command(description="reloads cog")
    async def reload(self, ctx, cog):
        self.bot.reload_extension(f"core.{cog}")
        embed = discord.Embed(title="Reload", description=f"{cog} successfully reloaded", color=utils.DEFAULT_COLOR)
        await ctx.respond(embed=embed)
        
def setup(bot):
    bot.add_cog(Dev(bot))