"""
Owner Commands
"""

import logging
import hikari
import lightbulb

# pylint: disable=no-name-in-module, import-error, unused-import
from wolfiebot.database.database import Database

log = logging.getLogger(__name__)
plugin = lightbulb.Plugin("commands.owner")
database = Database()

@plugin.command
@lightbulb.command("owner", "Owner commands")
@lightbulb.implements(lightbulb.PrefixCommandGroup, lightbulb.SlashCommandGroup)
# pylint: disable=unused-argument
async def owner(ctx: lightbulb.Context):
    """
    Handles owner commands.

    Args:
        ctx (lightbulb.Context): The context object representing the invocation.

    Returns:
        None:
    """
    return None

@owner.child
@lightbulb.command("set", "Set commands")
@lightbulb.implements(lightbulb.PrefixSubGroup, lightbulb.SlashSubGroup)
# pylint: disable=unused-argument
async def _set(ctx: lightbulb.Context):
    """
    Handles owner set commands.

    Args:
        ctx (lightbulb.Context): The context object representing the invocation.

    Returns:
        None:
    """
    return None

@_set.child
@lightbulb.option("role", "Select the admin role", type=hikari.Role, required=True)
@lightbulb.command("admin", "Set's the admin role")
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def set_admin(ctx: lightbulb.Context):
    """Sets the admin role for the guild.

    This command can only be executed by the guild owner.

    Args:
        ctx (lightbulb.Context): The context object representing the invocation.

    Returns:
        None:
    """
    if ctx.get_guild().owner_id != ctx.author.id:
        return

    role = ctx.options.role
    database.edit_guild_data(ctx.get_guild().id, "admin_role", role.id)
    await ctx.respond(notify(f"Admin role set {role.name}"))

def notify(message):
    """
    Creates an embed notification.

    Args:
        message (str): The message to be displayed in the embed.

    Returns:
        hikari.Embed: The embed object with the provided message.
    """
    embed = hikari.Embed(title=message, description="", color=0x00bfff)
    embed.set_author(name="Owner Tools", icon=plugin.bot.get_me().display_avatar_url)
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
