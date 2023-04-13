import logging
import hikari
import wolfiebot
import lightbulb
import pytz

from wolfiebot.database.database import Database

log = logging.getLogger(__name__)
plugin = lightbulb.Plugin("core.logs")
db = Database()

time_format = "%b %m, %Y @ %I:%M:%S%p %Z"

REMOVE_COLOR = 0xFFFFFF
ADDITION_COLOR = 0x2ECC71
CHANGE_COLOR = 0x1ABC9C
IMPORTANT_COLOR = 0xE74C3C

@plugin.listener(hikari.MemberCreateEvent)
async def member_join(event):
    member = event.user
    guild_id = event.guild_id
    embed = hikari.Embed(color=ADDITION_COLOR, title="Member Joined", description=f"{member} joined")
    embed.set_author(name=f"{member}", icon=member.display_avatar_url)
    embed.add_field(name=f"Account created", value=member.created_at.astimezone(pytz.timezone("America/New_York")).strftime(time_format))
    embed.set_footer(text=f"Account ID: {member.id}")
    await plugin.bot.rest.create_message(db.read_guild_data(guild_id, "logs_channel"), embed)
    
@plugin.listener(hikari.MemberDeleteEvent)
async def member_leave(event):
    member = event.user 
    guild_id = event.guild_id
    try:
        await event.app.rest.fetch_ban(guild_id, member)
        return
    except hikari.errors.NotFoundError:
        pass
    embed = hikari.Embed(color=REMOVE_COLOR, title="Member Left", description=f"{member} has left")
    embed.set_author(name=f"{member}", icon=member.display_avatar_url)
    embed.set_footer(text=f"Account ID: {member.id}")
    await plugin.bot.rest.create_message(db.read_guild_data(guild_id, "logs_channel"), embed)
    
def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)