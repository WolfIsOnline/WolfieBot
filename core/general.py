import discord

from discord.ext import commands
from discord.commands import slash_command
from classes.utils import Utils

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils()

    @slash_command(description="Get users profile picture")
    async def pfp(self, ctx, user: discord.User):
        avatar = discord.Embed(color=self.utils.DEFAULT_COLOR)
        avatar.set_image(url=user.display_avatar)
        await ctx.respond(embed=avatar)

def setup(bot):
    bot.add_cog(General(bot))