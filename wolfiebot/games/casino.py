import hikari
import lightbulb
import logging
import wolfiebot

from wolfiebot.core.casino import Casino
from wolfiebot.core.bank import Bank

plugin = lightbulb.Plugin("games.casino")
_casino = Casino()
bank = Bank()


# Admin Group
@plugin.command
@lightbulb.command("casino", "Casino commands")
@lightbulb.implements(lightbulb.PrefixCommandGroup, lightbulb.SlashCommandGroup)
async def casino(ctx: lightbulb.Context): pass

@casino.child
@lightbulb.command("balance", "Check balance")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def balance(ctx: lightbulb.Context): 
    author_id = ctx.author.id
    balance = _casino.get_balance(author_id)
    description = f"Credits: **{wolfiebot.CASINO_SYMBOL}{balance:,}**"
    embed = hikari.Embed(title="Nocturnia Casino", description=description, color=wolfiebot.CASINO_COLOR)
    embed.set_author(name=f"{ctx.author} | Member", icon=ctx.author.display_avatar_url)
    await ctx.respond(embed)
    

@casino.child
@lightbulb.option("amount", "Amount to deposit", type=int, required=True)
@lightbulb.command("deposit", "Deposit money into casino")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def deposit(ctx: lightbulb.Context): 
    author_id = ctx.author.id
    withdrawl = bank.withdraw(author_id, ctx.options.amount, "nocturnia casino")
    if withdrawl == -1:
        await ctx.respond("Transaction declined (Insufficient Funds)")
        return
    
    _casino.deposit(author_id, withdrawl)
    balance = _casino.get_balance(author_id)
    description = f"**{withdrawl:,}** credits have been added to your account"
    embed = hikari.Embed(title="Nocturnia Casino", description=description, color=wolfiebot.CASINO_COLOR)
    embed.add_field("Credits:", f"**{wolfiebot.CASINO_SYMBOL}{balance:,}**")
    await ctx.respond(embed)
    
@casino.child
@lightbulb.option("amount", "Amount to payout", type=int, required=True)
@lightbulb.command("payout", "Payout casino money to your bank account")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def payout(ctx: lightbulb.Context): 
    author_id = ctx.author.id
    balance = _casino.get_balance(author_id)
    if balance < 1:
        await ctx.respond("There is no money to payout")
        return
    
    if ctx.options.amount > balance:
        await ctx.respond(f"Amount requested is greater than your available payout")
        return
    
    confirmed_amount = _casino.withdraw(author_id, ctx.options.amount)
    bank.deposit(author_id, confirmed_amount, "Nocturnia Casino payout")
    await ctx.respond(f"**{wolfiebot.CURRENCY_SYMBOL}{ctx.options.amount:,}** has been transfered to your bank")
    
def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)