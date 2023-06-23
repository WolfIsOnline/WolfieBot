import hikari
import lightbulb
import logging
import wolfiebot

from wolfiebot.core.bank import Bank
from lightbulb import commands, GlobalBucket

log = logging.getLogger(__name__)
bank = Bank()
plugin = lightbulb.Plugin("commands.economy")

@plugin.command
@lightbulb.command("balance", "Display your balance")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def balance(ctx: lightbulb.Context):
    balance = bank.get_balance(ctx.author.id)
    embed = hikari.Embed(title = "Nocturnia Bank", description=f"Available Balance: **{wolfiebot.CURRENCY_SYMBOL}{balance:,}**", color=wolfiebot.DEFAULT_COLOR)
    embed.set_author(name=f"{ctx.author}", icon=ctx.author.display_avatar_url)
    await ctx.respond(embed)
    
@plugin.command
@lightbulb.add_cooldown(length=14400, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("payday", f"Get paid {wolfiebot.PAYDAY:,}")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand) 
async def payday(ctx: lightbulb.Context):
    bank.deposit(ctx.author.id, wolfiebot.PAYDAY, "payday")
    await ctx.respond(notify(f"{wolfiebot.CURRENCY_SYMBOL}{wolfiebot.PAYDAY:,} has been deposited into your account"))
    
@plugin.command
@lightbulb.option("user", "Select the member", type=hikari.User, required=True)
@lightbulb.option("amount", "Amount of money", type=int, required=True)
@lightbulb.command("transfer", "Transfer money to a member", aliases="tr")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def transfer(ctx: lightbulb.Context):
    amount = ctx.options.amount
    transfer_amount = bank.transfer(ctx.author.id, ctx.options.user.id, amount, f"Transfer to {ctx.options.user}", f"Transfer from {ctx.author}")
    log.debug(f"transfer {transfer_amount:,}")
    if transfer_amount <= -1:
        description = "Transfer declined (Insufficent Funds)"
    else:
        description = f"{wolfiebot.CURRENCY_SYMBOL}{amount:,} transfered to {ctx.options.user}"
    await ctx.respond(notify(description))
    
def notify(message):
    embed = hikari.Embed(title=message, description="", color=wolfiebot.DEFAULT_COLOR)
    embed.set_author(name=f"Nocturnia Bank", icon=plugin.bot.get_me().display_avatar_url)
    return embed 

def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)