"""
Logging server events
"""
import logging
import hikari
import lightbulb
import pytz
# pylint: disable=no-name-in-module, import-error
from wolfiebot.database.database import Database

log = logging.getLogger(__name__)
plugin = lightbulb.Plugin("core.logs")
database = Database()

TIME_FORMAT = "%b %m, %Y @ %I:%M:%S%p %Z"

REMOVE_COLOR = 0xFFFFFF
ADDITION_COLOR = 0x2ECC71
CHANGE_COLOR = 0x1ABC9C
IMPORTANT_COLOR = 0xE74C3C


@plugin.listener(hikari.MemberCreateEvent)
async def member_join(event) -> None:
    """
    Handles the member join event.

    Args:
        event: The member join event.

    Returns:
        None
    """
    member = event.user
    guild_id = event.guild_id
    embed = hikari.Embed(color=ADDITION_COLOR,
                         title="Member Joined", description=f"{member} joined")
    embed.set_author(name=f"{member}", icon=member.display_avatar_url)
    embed.add_field(name="Account created", value=member.created_at.astimezone(
        pytz.timezone("America/New_York")).strftime(TIME_FORMAT))
    embed.set_footer(text=f"Account ID: {member.id}")
    await plugin.bot.rest.create_message(database.read_guild_data(guild_id, "logs_channel"), embed)


@plugin.listener(hikari.MemberDeleteEvent)
async def member_leave(event) -> None:
    """
    Handles the member leave event.

    Args:
        event: The member leave event.

    Returns:
        None
    """
    member = event.user
    guild_id = event.guild_id
    try:
        await event.app.rest.fetch_ban(guild_id, member)
        return
    except hikari.errors.NotFoundError:
        pass
    embed = hikari.Embed(color=REMOVE_COLOR,
                         title="Member Left", description=f"{member} has left")
    embed.set_author(name=f"{member}", icon=member.display_avatar_url)
    embed.set_footer(text=f"Account ID: {member.id}")
    await plugin.bot.rest.create_message(database.read_guild_data(guild_id, "logs_channel"), embed)


@plugin.listener(hikari.GuildMessageUpdateEvent)
async def member_edit(event) -> None:
    """
    Handles the member edit event.

    Args:
        event: The member edit event.

    Returns:
        None
    """
    member = event.author
    if member.is_bot is True:
        return

    guild_id = event.guild_id
    embed = hikari.Embed(color=CHANGE_COLOR, title="Message Edited")
    embed.add_field("Original:", event.old_message.content)
    embed.add_field("New:", event.message.content)
    embed.set_author(name=f"{member}", icon=member.display_avatar_url)
    embed.set_footer(text=f"Message ID: {event.message.id}")
    await plugin.bot.rest.create_message(database.read_guild_data(guild_id, "logs_channel"), embed)


@plugin.listener(hikari.GuildMessageDeleteEvent)
async def member_delete(event) -> None:
    """
    Handles the member delete event.

    Args:
        event: The member delete event.

    Returns:
        None
    """
    member = event.old_message.author
    if member.is_bot is True:
        return
    guild_id = event.guild_id
    embed = hikari.Embed(color=REMOVE_COLOR, title="Message Deleted",
                         description=event.old_message.content)
    embed.add_field("Channel:", f"<#{event.channel_id}>")
    embed.set_author(name=f"{member}", icon=member.display_avatar_url)
    embed.set_footer(text=f"Message ID: {event.old_message.id}")
    await plugin.bot.rest.create_message(database.read_guild_data(guild_id, "logs_channel"), embed)

def load(bot: lightbulb.BotApp) -> None:
    """
    Loads the plugin into the bot.

    Args:
        bot (lightbulb.BotApp): The bot instance.

    Returns:
        None
    """
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp) -> None:
    """
    Unloads the plugin from the bot.

    Args:
        bot (lightbulb.BotApp): The bot instance.

    Returns:
        None
    """
    bot.remove_plugin(plugin)
