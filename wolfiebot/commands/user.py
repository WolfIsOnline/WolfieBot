"""
User Commands
"""

import logging
import random
import hikari
import lightbulb
import wolfiebot

# pylint: disable=no-name-in-module, import-error
from wolfiebot.database.database import Database

log = logging.getLogger(__name__)
plugin = lightbulb.Plugin("commands.user")
database = Database()

@plugin.command
@lightbulb.option("user", "Select a member", type=hikari.User, required=False)
@lightbulb.command("avatar", "Get users avatar", aliases="pfp")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def avatar(ctx: lightbulb.Context):
    """
    Get the avatar URL of a user.

    If no user is specified, it will return the avatar URL of the invoking user.

    Args:
        ctx (lightbulb.Context): The context object representing the invocation.

    Returns:
        None
    """
    try:
        avatar_url = ctx.options.user.display_avatar_url

    except AttributeError:
        avatar_url = ctx.author.display_avatar_url

    await ctx.respond(f"{avatar_url}")


@plugin.command
@lightbulb.option("user", "Select a member", type=hikari.User, required=False)
@lightbulb.command("quote", "Get a random quote")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def quote(ctx: lightbulb.Context):
    """
    Get a random quote.

    If a user is specified, it retrieves a random quote from that user.
    Otherwise, it retrieves a random quote from all quotes.

    Args:
        ctx (lightbulb.Context): The context object representing the invocation.

    Returns:
        None
    """
    quotes = database.read_guild_data(ctx.get_guild().id, "quotes")
    sorted_quote_data = []
    if ctx.options.user is not None:
        for raw_quote_data in quotes:
            if raw_quote_data["quote_user_id"] == ctx.options.user.id:
                log.info("appended")
                sorted_quote_data.append(raw_quote_data)
    else:
        sorted_quote_data = quotes

    random_quote = random.choice(sorted_quote_data)
    _quote = random_quote["quote"]
    if random_quote["quote_user"] != "Unknown":
        quote_user = "<@" + str(random_quote["quote_user_id"]) + ">"
    else:
        quote_user = "Unknown"

    await ctx.respond(f"\"{_quote}\" - {quote_user}")


def notify(message):
    """
    Create an embed notification.

    Args:
        message (str): The message to be displayed in the embed.

    Returns:
        hikari.Embed: The embed object with the provided message.
    """
    embed = hikari.Embed(title=message, description="",
                         color=wolfiebot.DEFAULT_COLOR)
    embed.set_author(name="Wolfie Commands",
                     icon=plugin.bot.get_me().display_avatar_url)
    return embed

def load(bot: lightbulb.BotApp):
    """
    Loads the plugin into the bot.

    Parameters:
    - bot (lightbulb.BotApp): The bot instance.

    """
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp):
    """
    Unloads the plugin from the specified bot.

    Args:
        bot (lightbulb.BotApp): The bot instance to unload the plugin from.

    Returns:
        None
    """
    bot.remove_plugin(plugin)
