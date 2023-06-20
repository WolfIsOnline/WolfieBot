import hikari
import lightbulb
import logging
import wolfiebot
import re

from wolfiebot.database.database import Database

log = logging.getLogger(__name__)
plugin = lightbulb.Plugin("core.quotes")
db = Database()

def validate(quote) -> bool:
    if quote:
        quote = quote[0]
        if quote == "" or quote.isspace():
            return False
        return True
    return False

def is_unknown(quote_user_id) -> bool:
    if quote_user_id:
        return False
    return True

async def commit(content, author_id, guild_id, ctx=None, fake_add=False):
    quote = re.split("\"", content)[1::2]
    quote_user_id = re.split("<@|>", content)[1::2]
    
    if validate(quote) is True:
        quote = quote[0]
        submitted_user = await plugin.bot.rest.fetch_user(author_id)
        if is_unknown(quote_user_id) is False:
            quote_user_id = quote_user_id[0]
            quote_user = await plugin.bot.rest.fetch_user(quote_user_id)
            desc_format = quote_user.mention
        else:
            quote_user = "Unknown"
            quote_user_id = "Unknown"
            desc_format = "Unknown"
        
        db.append_guild_data(guild_id, "quotes", {"quote" : quote, "quote_user_id" : quote_user_id, "quote_user" : str(quote_user), "submitted_user" : str(submitted_user), "submitted_user_id" : str(author_id)})
        print(f"quote [{quote}] added")
        total_quotes = len(db.read_guild_data(guild_id, "quotes"))
    '''
        embed = hikari.Embed(title="Quote Added", description=f"\"{quote}\" - {desc_format}", color=wolfiebot.DEFAULT_COLOR)
        embed.set_author(name=f"Quote #{total_quotes}")
        if ctx is None:
            await plugin.bot.rest.create_message(db.read_guild_data(guild_id, "quotes_channel"), embed)
        else:
            await ctx.respond(embed)
    '''

@plugin.listener(hikari.GuildMessageCreateEvent)
async def listen(event):
    channel_id = db.read_guild_data(event.guild_id, "quotes_channel")
    if event.channel_id != channel_id or event.is_bot is True or not event.content.startswith("\""):
        return
    await commit(event.content, event.author_id, event.guild_id)

def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)