import random

from discord.ext import commands
from discord.commands import slash_command
from classes.utils import Utils
from database.database import GuildDatabase

gd = GuildDatabase()


class Quotes(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils()

    async def set_quotes(self, guild_id, channel_id):
        gd.update_guild_key(guild_id, "quotes_channel", channel_id)

    async def force_refresh(self, guild_id):
        channel = self.bot.get_channel(int(gd.get_guild_key(guild_id, "quotes_channel")))
        quotes = await channel.history(limit=10000).flatten()
        size = 0
        with open("quotes.log", "w") as log:
            for i in quotes:
                if i.content.startswith('\"') or i.content.startswith('“'):
                    size += 1
                    log.write(i.content + "\n")

    async def add_quote(self, guild_id, message):
        contents = message.content
        channel = self.bot.get_channel(int(gd.get_guild_key(guild_id, "quotes_channel")))
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
        
        guild_id = message.guild.id
        if message.channel.id == int(gd.get_guild_key(message.guild.id, "quotes_channel")):
            await self.add_quote(guild_id, message)

    @slash_command(description="Gets a random quote submitted by Members")
    async def quote(self, ctx):
        with open("quotes.log", "r") as log:
            quotes = log.readlines()
            index = random.randrange(len(quotes))
            await ctx.respond(quotes[index])


def setup(bot):
    bot.add_cog(Quotes(bot))
