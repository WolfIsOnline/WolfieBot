"""
User Commands
"""
import sys
import logging
import hikari
import lightbulb
# pylint: disable=no-name-in-module, import-error
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
@lightbulb.command("info", "Info about Wolfie")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def info(ctx: lightbulb.Context):
    """
    Provides information about the Wolfie bot.

    Args:
        ctx (lightbulb.Context): The command context.
    """
    python_version = sys.version_info
    embed = hikari.Embed(
        title="About Wolfie",
        description=wolfiebot.__description__,
        color=wolfiebot.DEFAULT_COLOR
    )
    embed.add_field("Wolfie version", wolfiebot.__version__, inline=True)
    embed.add_field("Python", f"[{python_version.major}.{python_version.minor}.{python_version.micro}](https://python.org)", inline=True)
    embed.add_field("Hikari", f"[{hikari.__version__}](https://github.com/hikari-py/hikari)", inline=True)
    await ctx.respond(embed=embed)


@plugin.command
@lightbulb.option("user", "Select a member", type=hikari.User, required=False)
@lightbulb.command("profile", "Info about Wolfie")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def profile(ctx: lightbulb.Context):
    user_id = ctx.author.id
    embed = hikari.Embed(
        title=f"{ctx.author}'s Profile",
        color=wolfiebot.DEFAULT_COLOR
    )
    embed.add_field("Level", database.read_user_data(user_id, "level"), inline=True)
    embed.add_field("XP", database.read_user_data(user_id, "xp"), inline=True)
    embed.add_field("Balance", database.read_user_data(user_id, "balance"))
    embed.add_field("Casino Balance", database.read_user_data(user_id, "casino_balance"))


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
