import hikari
import lightbulb
import logging
import wolfiebot

from lightbulb import commands
from wolfiebot.database.database import Database

log = logging.getLogger(__name__)
plugin = lightbulb.Plugin("commands.admin")
database = Database()

# need to implement admin role
#admin_role = database.read_guild_data(guild_id)

# Admin Group
@plugin.command
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command("admin", "Admin commands")
@lightbulb.implements(lightbulb.PrefixCommandGroup, lightbulb.SlashCommandGroup)
async def admin(ctx: lightbulb.Context): pass

@admin.child
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command("set", "Set commands")
@lightbulb.implements(lightbulb.PrefixSubGroup, lightbulb.SlashSubGroup)
async def _set(ctx: lightbulb.Context): pass

# Set Command Group
@_set.child
@lightbulb.option("channel", "Select the quotes channel", type=hikari.TextableChannel, required=True)
@lightbulb.command("quotes", "Set quotes channel")
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def quotes(ctx: lightbulb.Context):
    channel = ctx.options.channel
    database.edit_guild_data(ctx.get_guild().id, "quotes_channel", channel.id)
    await ctx.respond(f"Quotes channel set to {channel.mention}")
    
@_set.child
@lightbulb.option("channel", "Select the voice channel", type=hikari.GuildVoiceChannel, required=True)
@lightbulb.command("room", "Set parent room channel")
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def room(ctx: lightbulb.Context):
    channel = ctx.options.channel
    database.edit_guild_data(ctx.get_guild().id, "autoroom_parent", channel.id)
    await ctx.respond(f"Parent channel set to {channel.mention}")
    
@_set.child
@lightbulb.option("channel", "Select the logs channel", type=hikari.TextableChannel, required=True)
@lightbulb.command("logs", "Set logs channel")
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def logs(ctx: lightbulb.Context):
    channel = ctx.options.channel
    database.edit_guild_data(ctx.get_guild().id, "logs_channel", channel.id)
    await ctx.respond(f"Logs channel set to {channel.mention}")
    
@_set.child
@lightbulb.option("channel", "Select the welcome channel", type=hikari.TextableChannel, required=True)
@lightbulb.command("welcome", "Set the welcome channel")
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def welcome(ctx: lightbulb.Context):
    channel = ctx.options.channel
    database.edit_guild_data(ctx.get_guild().id, "welcome_channel", channel.id)
    await ctx.respond(f"Welcome channel set to {channel.mention}")   
# End of set

@admin.child
@lightbulb.option("message_id", "Input the message ID", type=str, required=True)
@lightbulb.command("savequote", "Saves quote from message ID")
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def save_quote(ctx: lightbulb.Context):
    message = await plugin.bot.rest.fetch_message(ctx.channel_id, ctx.options.message_id)
    await wolfiebot.core.quotes.commit(message.content, message.author.id, ctx.get_guild().id, ctx)
    
@admin.child
@lightbulb.option("role", "Select the role", type=hikari.Role)
@lightbulb.command("addrole", "Adds autorole to list")
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def add_role(ctx: lightbulb.Context):
    role = ctx.options.role
    roles = database.read_guild_data(ctx.get_guild().id, "autoroles")
    if roles is not None:
        for _role in roles:
            if _role == role.id:
                await ctx.respond(f"{role.mention} has already been added!")
                return
    database.append_guild_data(ctx.get_guild().id, "autoroles", role.id)
    await ctx.respond(f"{role.mention} added")
    
@admin.child
@lightbulb.option("role", "Select the role", type=hikari.Role)
@lightbulb.command("removerole", "Removes autorole from list")
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def remove_role(ctx: lightbulb.Context):
    role = ctx.options.role
    database.remove_guild_data_array(ctx.get_guild().id, "autoroles", role.id)
    await ctx.respond(f"{role.mention} removed")

def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)