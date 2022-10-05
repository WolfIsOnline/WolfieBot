import random

from discord.ext import commands
from discord.commands import slash_command
from classes.utils import Utils
from database.database import GuildDatabase

GUILD_ID = 851644348281258035
gd = GuildDatabase()


class Quotes(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils()

    async def set_quotes(self, channel_id):
        gd.update_guild_key(GUILD_ID, "quotes_channel", channel_id)

    async def force_refresh(self):
        channel = self.bot.get_channel(int(gd.get_guild_key(GUILD_ID, "quotes_channel")))
        quotes = await channel.history(limit=10000).flatten()
        size = 0
        with open("quotes.log", "w") as log:
            for i in quotes:
                if i.content.startswith('\"') or i.content.startswith('“'):
                    size += 1
                    log.write(i.content + "\n")

    async def add_quote(self, message):
        contents = message.content
        channel = self.bot.get_channel(int(gd.get_guild_key(GUILD_ID, "quotes_channel")))
        size = 0
        with open("quotes.log", "a") as log:
            if contents.startswith('\"') or message.startswith('“'):
                size += 1
                log.write(contents + "\n")
                with open("quotes.log", "r") as log_read:
                    temp = str(len(log_read.readlines()))    
                await self.utils.notify_channel(channel, "Quote Added", contents, f"Quote #{temp}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.channel.id == int(gd.get_guild_key(GUILD_ID, "quotes_channel")):
            await self.add_quote(message)

    @slash_command(description="Gets a random quote submitted by Members")
    async def quote(self, ctx):
        with open("quotes.log", "r") as log:
            quotes = log.readlines()
            index = random.randrange(len(quotes))
            await ctx.respond(quotes[index])


def setup(bot):
    bot.add_cog(Quotes(bot))
