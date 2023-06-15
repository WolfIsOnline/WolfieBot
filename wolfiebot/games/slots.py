import logging
import hikari
import wolfiebot
import lightbulb
import random
import asyncio
import json

from wolfiebot.database.database import Database
from wolfiebot.core.casino import Casino

log = logging.getLogger(__name__)
plugin = lightbulb.Plugin("games.slots")
database = Database()
casino = Casino()
credit_symbol = "₵"

@plugin.command
@lightbulb.option("amount", "Amount to bet", type=int, required=True)
@lightbulb.command("slots", "Slots")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def slots(ctx: lightbulb.Context):
    if ctx.options.amount < 2:
        await ctx.respond("You must bet at least **₵2 credits**")
        return
    
    if casino.get_balance(ctx.author.id) <= 0 or casino.get_balance(ctx.author.id) < ctx.options.amount:
        await ctx.respond("You don't have enough credits. Please deposit more")
        return
    
    casino.withdraw(ctx.author.id, ctx.options.amount)
        
    animation  = get_animation_symbol()
    await ctx.respond(f"{animation['format']} | {animation['format']} | {animation['format']}")
    
    slots = []
    for c in range(3):
        slots.append(animation)
    for c in range(3):
        await asyncio.sleep(.3)
        slots[c] = get_choice()
        await ctx.edit_last_response(f"{slots[0]['format']} | {slots[1]['format']} | {slots[2]['format']}")
    
    slot_names = []
    for slot in slots:
        slot_names.append(slot["name"])
    payout = get_payout(slot_names)
    payout_amount = payout * ctx.options.amount
    casino.deposit(ctx.author.id, payout_amount)
    if payout == 0:
        message = "You lost!"
        sign = "-"
        amount = ctx.options.amount
        color = 0xFF0000
    else:
        message = "YOU WON!"
        sign = "+"
        amount = payout_amount
        color = 0x2ECC71    
    embed = hikari.Embed(title="Nocturnia Casino", color=color)
    embed.add_field("Result:", f"{slots[0]['format']} | {slots[1]['format']} | {slots[2]['format']}")
    embed.add_field("Credits:", f"**₵{casino.get_balance(ctx.author.id):,}**")
    await ctx.edit_last_response(f"{message} **{sign}₵{amount:,}**", embed=embed)
    
    
def get_payout(slots):
    # cherries
    count = 0
    for symbol in slots:
        if symbol == "cherry":
            count += 1
    if count == 1: return 2
    elif count == 2: return 5
    elif count == 3: return 10
    
    # bars
    count = 0
    for symbol in slots:
        if symbol == "bar":
            count += 1
    if count == 3: return 10
    
    # sevens
    count = 0
    for symbol in slots:
        if symbol == "seven":
            count += 1
    if count == 3: return 100
    
    # diamonds
    count = 0
    for symbol in slots:
        if symbol == "diamond":
            count += 1
    if count == 3: return 1600
        
    return 0
    
def get_static_symbol(filter_by, search):
    symbols = get_symbols()["static"]
    for index, symbol in enumerate(symbols):
        if search is not None:
            if symbol[filter_by] == search:
                return symbols[index]
        else:
            return symbols
        
def get_animation_symbol():
    return get_symbols()["animation"]
    
def get_symbols():
    with open("/home/wolf/Projects/WolfieBot-2.0/wolfiebot/games/symbols.json") as file:
        data = json.load(file)
    return data   
    
def get_choice():
    symbols = get_static_symbol(filter_by=None, search=None)
    weights = []
    for symbol in symbols:
        weights.append(symbol["weight"])
    return random.choices(symbols, weights=tuple(weights))[0]
    
def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
