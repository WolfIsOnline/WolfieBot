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
    await ctx.respond(embed)
    

@casino.child
@lightbulb.option("amount", "Amount of money", type=int, required=True)
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
    
    
def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)