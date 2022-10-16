import discord
import sys

from discord.ext import commands
from discord.commands import slash_command
from classes.utils import Utils


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils()

    @slash_command(description="information for nerds")
    async def info(self, ctx):
        python_version = sys.version
        pycord = "development version"
        creator = "WolfIsOnline#6677"
        bot_version = "1.1.1-alpha"
        info = discord.Embed(color=self.utils.DEFAULT_COLOR)
        info.set_author(name="Wolfie#1704", icon_url="https://cdn.discordapp.com/avatars/1021246946649849867/118da25b10cf765d4472c4664df8dd63.png?size=1024")
        info.add_field(name="Bot created by", value=creator)
        info.add_field(name="Python", value=python_version)
        info.add_field(name="Pycord", value=pycord)
        info.add_field(name="Wolfie version", value=bot_version)

        await ctx.respond(embed=info)


def setup(bot):
    bot.add_cog(Info(bot))
