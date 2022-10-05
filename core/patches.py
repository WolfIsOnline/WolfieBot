import discord

from discord import slash_command
from discord.ext import commands
from classes.utils import Utils


class Patches(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils()

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.channel.id == 1024949304546316299:
            return
        if message.author.id == 1021246946649849867:
            return

        original = message.embeds
        data = None
        for m in original:
            data = m.to_dict()

        try:
            if data["title"] == "PatchBot can now notify you of free games" or data["title"] == "Pinned Updates with PatchBot Premium":
                return
            title = data["title"]
        except:
            title = ""

        try:
            description = data["description"]
        except:
            description = ""

        try:
            author = data["author"]["name"]
        except:
            author = ""

        try:
            thumbnail = data["thumbnail"]["url"]
        except:
            thumbnail = ""

        try:
            image = data["image"]["url"]
        except:
            image = ""

        try:
            fields = []
            fields = data["fields"]
        except:
            fields = []

        duplicate = discord.Embed(title=title, description=description, color=self.utils.DEFAULT_COLOR)
        duplicate.set_author(name=author)
        duplicate.set_thumbnail(url=thumbnail)
        duplicate.set_image(url=image)

        for c in fields:
            duplicate.add_field(name=c["name"], value=c["value"], inline=c["inline"])

        if author == "Epic Games" or author == "Steam" or author == "GOG":
            channel = self.bot.get_channel(967074827108245554)
        else:
            channel = self.bot.get_channel(973745210016280577)
        await channel.send(embed=duplicate)


def setup(bot):
    bot.add_cog(Patches(bot))
