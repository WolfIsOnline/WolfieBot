"""
User Commands
"""
import logging
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
