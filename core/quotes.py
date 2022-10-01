import random


from discord.ext import commands
from discord.commands import slash_command
from classes.utils import Utils
from database.database import Guild_DataBase

GUILD_ID = 851644348281258035
gd = Guild_DataBase()

class Quotes(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils()

    async def setquotes(self, id):
        gd.update_guild_key(GUILD_ID, "quotes_channel", id)

    async def force_refresh(self):
        channel = self.bot.get_channel(int(gd.get_guild_key(GUILD_ID, "quotes_channel")))
        quotes = await channel.history(limit=10000).flatten()
        size = 0
        log = open("quotes.log", "w")
        for i in quotes:
            if i.content.startswith('\"') or i.content.startswith('“'):
                size += 1
                log.write(i.content + "\n")
        log.close()

    async def add_quote(self, message):
        channel = self.bot.get_channel(int(gd.get_guild_key(GUILD_ID, "quotes_channel")))
        quotes = await channel.history(limit=1).flatten()
        size = 0
        log = open("quotes.log", "a")
        for i in quotes:
            if i.content.startswith('\"') or i.content.startswith('“'):
                size += 1
                log.write(i.content + "\n")
                log.close()    
                log_read = open("quotes.log", "r")
                temp = str(len(log_read.readlines()))
                await self.utils.notify_channel(channel, "Quote Added", i.content, f"Quote #{temp}")
                log_read.close()
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.channel.id == int(gd.get_guild_key(GUILD_ID, "quotes_channel")):
            await self.add_quote(message)

    @slash_command(description="Gets a random quote submitted by Members")
    async def quote(self, ctx):
        log = open("quotes.log", "r")
        quotes = log.readlines()
        index = random.randrange(len(quotes))
        await ctx.respond(quotes[index])

def setup(bot):
    bot.add_cog(Quotes(bot))