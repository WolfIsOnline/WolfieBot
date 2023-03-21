import hikari
import lightbulb
import logging
import wolfiebot

from lightbulb import commands
from wolfiebot.core.bank import Bank
from wolfiebot.database.database import Database

log = logging.getLogger(__name__)
plugin = lightbulb.Plugin("commands.user")
bot = lightbulb.BotApp
db = Database()


@plugin.command
@lightbulb.option("user", "Select the member", type=hikari.User, required=False)
@lightbulb.command("avatar", "Get users avatar", aliases="pfp")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def avatar(ctx: lightbulb.Context):
    try:
        user = ctx.options.user
        avatar_url = ctx.options.user.display_avatar_url
        
    except AttributeError:
        user = ctx.author
        avatar_url = ctx.author.display_avatar_url
        
    embed = hikari.Embed(color=wolfiebot.DEFAULT_COLOR, title=user, description=f"{avatar_url}")
    embed.set_image(avatar_url)
    
    await ctx.respond(embed)
    
@plugin.command
@lightbulb.command("quote", "Get a random quote")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def quote(ctx: lightbulb.Context):
    
    user = await plugin.bot.rest.fetch_user("257646822925926410")
    log.info(user)
    quote = db.read_guild_data(ctx.get_guild().id, "quotes")
    log.info(quote[0]["quote"])
    await ctx.message.respond("hi")
    
def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
