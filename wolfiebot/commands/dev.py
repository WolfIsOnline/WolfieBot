import hikari
import lightbulb
import logging
import wolfiebot

from lightbulb import commands
from wolfiebot.core.bank import Bank

log = logging.getLogger(__name__)
plugin = lightbulb.Plugin("commands.dev")


@plugin.command
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.option("amount", "Amount to deposit", type=int, required=True)
@lightbulb.command("deposit", "Deposit from member")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def deposit(ctx: lightbulb.Context):
    Bank().deposit(ctx.author.id, ctx.options.amount)
    await ctx.respond(ctx.options.amount)
    
@plugin.command
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.option("amount", "Amount to withdraw", type=int, required=True)
@lightbulb.command("withdraw", "Withdraw from member")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def withdraw(ctx: lightbulb.Context):
    amount = Bank().withdraw(ctx.author.id, ctx.options.amount)
    await ctx.respond(amount)

def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)