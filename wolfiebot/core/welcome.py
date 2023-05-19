import logging
import hikari
import wolfiebot
import lightbulb

from wolfiebot.database.database import Database

log = logging.getLogger(__name__)
plugin = lightbulb.Plugin("core.welcome")
db = Database()

@plugin.listener(hikari.MemberCreateEvent)
async def member_join(event):
    member = event.user
    guild_id = event.guild_id
    guild = plugin.bot.cache.get_guild(guild_id)
    embed = hikari.Embed(color=wolfiebot.DEFAULT_COLOR, title="Welcome to Nocturnal Gamers", description=f"Hi {member.mention}\n\n• **I hope you enjoy your stay!**\n\n• **Check out the following channels.**\n\n<a:ng_bluearrowright:996149975471902760> Current free games <#967074827108245554>\n\n<a:ng_bluearrowright:996149975471902760> Newest <#973745210016280577>",)
    embed.set_author(name=f"{guild}", icon=guild.icon_url)
    embed.set_thumbnail(member.display_avatar_url)
    try:
        embed.set_image(guild.banner_url)
    except:
        pass
    
    await plugin.bot.rest.create_message(db.read_guild_data(guild_id, "welcome_channel"), embed)
    
def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
