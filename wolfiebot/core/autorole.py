import logging
import hikari
import wolfiebot
import lightbulb

from wolfiebot.database.database import Database

log = logging.getLogger(__name__)
plugin = lightbulb.Plugin("core.autorole")
db = Database()

@plugin.listener(hikari.MemberCreateEvent)
async def member_join(event):
    member = event.member
    guild_id = event.guild_id
    guild = plugin.bot.cache.get_guild(guild_id)
    roles = db.read_guild_data(guild_id, "autoroles")
    if roles is not None:
        for _role in roles:
            role = plugin.bot.cache.get_role(_role)
            await member.add_role(role)

def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)