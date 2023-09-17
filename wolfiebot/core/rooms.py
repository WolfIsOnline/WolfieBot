"""
Auto Room Module
"""
import logging
import hikari
import lightbulb
from hikari.permissions import Permissions
# pylint: disable=no-name-in-module, import-error
from wolfiebot.database.database import Database

log = logging.getLogger(__name__)
plugin = lightbulb.Plugin("core.rooms")
database = Database()

@plugin.listener(hikari.VoiceStateUpdateEvent)
async def listen(event):
    """
    Listens for voice state update events and creates a new voice room if necessary.

    Args:
        event: The event object representing the voice state update event.

    Returns:
        None
    """
    parent_channel_id = database.read_guild_data(event.guild_id, "autoroom_parent")
    if event.state.channel_id != parent_channel_id:
        return

    await create_room(event, parent_channel_id)

@plugin.listener(hikari.VoiceStateUpdateEvent)
async def check_empty(event):
    """
    Listens for voice state update events and deletes empty autoroom channels.

    Args:
        event: The event object representing the voice state update event.

    Returns:
        None
    """
    if event.old_state is None:
        return
    channels = database.read_guild_data(event.guild_id, "autoroom_channels")
    for _id in channels:
        if event.old_state.channel_id == _id:
            channel = plugin.bot.cache.get_guild_channel(_id)
            members = plugin.bot.cache.get_voice_states_view_for_channel(event.guild_id, channel)
            if len(members) == 0:
                await channel.delete()
                database.remove_guild_data_array(event.guild_id, "autoroom_channels", _id)

async def create_room(event, parent_channel_id):
    """
    Creates a new autoroom channel for a user.

    Args:
        event: The event object representing the voice state update event.
        parent_channel_id: The ID of the parent channel for autorooms.

    Returns:
        None
    """

    parent_channel = plugin.bot.cache.get_guild_channel(parent_channel_id)
    member = plugin.bot.cache.get_member(event.guild_id, event.state.user_id)
    name = member.nickname
    if member.nickname is None:
        name = member
    channel = await event.app.rest.create_guild_voice_channel(
            event.guild_id,
            f"{name}'s VC",
            user_limit=parent_channel.user_limit,
            bitrate=parent_channel.bitrate,
            video_quality_mode=parent_channel.video_quality_mode,
            region=parent_channel.region,
            category=parent_channel.parent_id,
            reason=f"Requested by {plugin.bot.get_me()}",
            permission_overwrites=[hikari.channels.PermissionOverwrite(
                id=event.state.user_id,
                type=hikari.channels.PermissionOverwriteType.MEMBER,
                allow=(Permissions.MANAGE_CHANNELS),
            )]
    )
    database.append_guild_data(event.guild_id, "autoroom_channels", channel.id)
    await plugin.bot.rest.edit_member(event.guild_id, event.state.user_id, voice_channel=channel.id)

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
