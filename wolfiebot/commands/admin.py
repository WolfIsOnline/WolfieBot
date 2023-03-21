import hikari
import lightbulb
import logging
import wolfiebot

from lightbulb import commands
from wolfiebot.database.database import Database

log = logging.getLogger(__name__)
plugin = lightbulb.Plugin("commands.admin")
db = Database()

@plugin.command
@lightbulb.option("channel", "Select the channel", type=hikari.TextableChannel, required=True)
@lightbulb.command("setquotes", "Set quotes channel")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def set_quotes(ctx: lightbulb.Context):
    channel = ctx.options.channel
    db.edit_guild_data(ctx.get_guild().id, "quotes_channel", channel.id)
    await ctx.respond(f"Quotes channel set to {channel.mention}")
    
@plugin.command
@lightbulb.option("channel", "Select the voice channel", type=hikari.GuildVoiceChannel, required=True)
@lightbulb.command("setroom", "Set parent room channel")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def set_room(ctx: lightbulb.Context):
    channel = ctx.options.channel
    db.edit_guild_data(ctx.get_guild().id, "autoroom_parent", channel.id)
    await ctx.respond(f"Room parent channel set to {channel.mention}")
    
@plugin.command
@lightbulb.option("channel", "Select the logs channel", type=hikari.TextableChannel, required=True)
@lightbulb.command("setlogs", "Set the logs channel")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def set_logs(ctx: lightbulb.Context):
    channel = ctx.options.channel
    db.edit_guild_data(ctx.get_guild().id, "logs_channel", channel.id)
    await ctx.respond(f"Logs channel set to {channel.mention}")

@plugin.command
@lightbulb.option("message_id", "Input the message ID", type=str, required=True)
@lightbulb.command("savequote", "Saves quote from message ID")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def save_quote(ctx: lightbulb.Context):
    message = await plugin.bot.rest.fetch_message(ctx.channel_id, ctx.options.message_id)
    await wolfiebot.core.quotes.commit(message.content, message.author.id, ctx.get_guild().id, ctx)

def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)