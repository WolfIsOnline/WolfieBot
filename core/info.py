from discord.ext import commands
from discord.commands import slash_command

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="information for nerds")
    async def info(self, ctx):
        python_version = sys.version
        pycord = "development version"
        creator = "WolfIsOnline#6677"
        botversion = "1.0.0a"
        info = discord.Embed(title="Wolfie Bot", color=0x02e7e7)
        info.set_thumbnail(url="https://cdn.discordapp.com/avatars/1021246946649849867/118da25b10cf765d4472c4664df8dd63.png?size=1024")
        info.add_field(name="Bot created by", value=creator)
        info.add_field(name="Python", value=python_version)
        info.add_field(name="Pycord", value=pycord)
        info.add_field(name="Wolfie version", value=botversion)

def setup(bot):
    bot.add_cog(Info(bot))