import hikari
import lightbulb
import logging
import wolfiebot

from hikari.permissions import Permissions
from wolfiebot.database.database import Database

log = logging.getLogger(__name__)
plugin = lightbulb.Plugin("commands.rooms")
db = Database()

@plugin.listener(hikari.VoiceStateUpdateEvent)
async def listen(event):
    parent_channel_id = db.read_guild_data(event.guild_id, "autoroom_parent")
    if event.state.channel_id != parent_channel_id:
        return
    
    await create_room(event, parent_channel_id)
    
@plugin.listener(hikari.VoiceStateUpdateEvent)
async def check_empty(event):
    if event.old_state is None:
        return
    channels = db.read_guild_data(event.guild_id, "autoroom_channels")
    for _id in channels:
        if event.old_state.channel_id == _id:
            channel = plugin.bot.cache.get_guild_channel(_id)
            members = plugin.bot.cache.get_voice_states_view_for_channel(event.guild_id, channel)
            if len(members) == 0:
                await channel.delete()
                db.remove_guild_data_array(event.guild_id, "autoroom_channels", _id)
    
async def create_room(event, parent_channel_id):
    parent_channel = plugin.bot.cache.get_guild_channel(parent_channel_id)
    member = plugin.bot.cache.get_member(event.guild_id, event.state.user_id)
    channel = await event.app.rest.create_guild_voice_channel(
            event.guild_id, 
            f"{member.username}'s Room", 
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
    db.append_guild_data(event.guild_id, "autoroom_channels", channel.id)
    await plugin.bot.rest.edit_member(event.guild_id, event.state.user_id, voice_channel=channel.id)
    
async def delete_empty(channel_id):
    pass

def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
    
    