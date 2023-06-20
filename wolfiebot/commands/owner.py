import hikari
import lightbulb
import logging
import wolfiebot

from wolfiebot.database.database import Database

log = logging.getLogger(__name__)
plugin = lightbulb.Plugin("commands.owner")
database = Database()

# Owner Group
@plugin.command
@lightbulb.command("owner", "Owner commands")
@lightbulb.implements(lightbulb.PrefixCommandGroup, lightbulb.SlashCommandGroup)
async def owner(ctx: lightbulb.Context): pass

@owner.child
@lightbulb.command("set", "Set commands")
@lightbulb.implements(lightbulb.PrefixSubGroup, lightbulb.SlashSubGroup)
async def _set(ctx: lightbulb.Context): pass

@_set.child
@lightbulb.option("role", "Select the admin role", type=hikari.Role, required=True)
@lightbulb.command("admin", "Set's the admin role")
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def set_admin(ctx: lightbulb.Context):
    if ctx.get_guild().owner_id != ctx.author.id:
        return
    
    role = ctx.options.role
    database.edit_guild_data(ctx.get_guild().id, "admin_role", role.id)
    await ctx.respond(notify(f"Admin role set {role.name}"))
    
def notify(message):
    embed = hikari.Embed(title=message, description="", color=0x00bfff)
    embed.set_author(name=f"Owner Tools", icon=plugin.bot.get_me().display_avatar_url)
    return embed 


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)