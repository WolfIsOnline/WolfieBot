import hikari
import lightbulb
import logging
import wolfiebot

from lightbulb import commands
from wolfiebot.core.bank import Bank
from wolfiebot.database.database import Database

log = logging.getLogger(__name__)
plugin = lightbulb.Plugin("commands.dev")
db = Database()

@plugin.command
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command("dev", "dev commands")
@lightbulb.implements(lightbulb.PrefixCommandGroup, lightbulb.SlashCommandGroup)
async def dev(ctx: lightbulb.Context): pass

@dev.child
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.option("amount", "Amount to deposit", type=int, required=True)
@lightbulb.command("deposit", "Deposit from member")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def deposit(ctx: lightbulb.Context):
    Bank().deposit(ctx.author.id, ctx.options.amount)
    await ctx.respond(ctx.options.amount)
    
@dev.child
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.option("amount", "Amount to withdraw", type=int, required=True)
@lightbulb.command("withdraw", "Withdraw from member")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def withdraw(ctx: lightbulb.Context):
    amount = Bank().withdraw(ctx.author.id, ctx.options.amount)
    await ctx.respond(amount)
    
@dev.child
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.option("status", "Status Messsage", type=str, required=True)
@lightbulb.command("setstatus", "Set bot status")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def set_status(ctx: lightbulb.Context):
    await plugin.bot.update_presence(status=hikari.Status.ONLINE, activity=hikari.Activity( name=ctx.options.status, type=hikari.ActivityType.PLAYING,),)
    db.edit_user_data(plugin.bot.get_me().id, "status", ctx.options.status)
    await ctx.respond("presence updated!")
    
@dev.child
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.option("extension", "Extension", type=str, required=True)
@lightbulb.command("load", "Load an entension")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def load_ext(ctx: lightbulb.Context):
    plugin.bot.load_extensions(f"wolfiebot.{ctx.options.extension}")
    await ctx.respond(f"{ctx.options.extension} loaded")
    
@dev.child
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.option("extension", "Extension", type=str, required=True)
@lightbulb.command("unload", "Unload an extension")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def unload_ext(ctx: lightbulb.Context):
    plugin.bot.unload_extensions(f"wolfiebot.{ctx.options.extension}")
    await ctx.respond(f"{ctx.options.extension} unloaded")
    
@dev.child
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.option("extension", "Extension", type=str, required=True)
@lightbulb.command("reload", "Reload an extension")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def reload_ext(ctx: lightbulb.Context):
    plugin.bot.unload_extensions(f"wolfiebot.{ctx.options.extension}")
    plugin.bot.load_extensions(f"wolfiebot.{ctx.options.extension}")
    await ctx.respond(f"{ctx.options.extension} reloaded")

def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)