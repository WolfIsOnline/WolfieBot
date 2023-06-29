import hikari
import lightbulb
import logging
import pprint
import wolfiebot
import asyncio
import psutil
import datetime

from lightbulb import commands
from wolfiebot.core.bank import Bank
from wolfiebot.database.database import Database

log = logging.getLogger(__name__)
plugin = lightbulb.Plugin("commands.dev")
database = Database()

@plugin.command
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command("dev", "dev commands")
@lightbulb.implements(lightbulb.PrefixCommandGroup, lightbulb.SlashCommandGroup)
async def dev(ctx: lightbulb.Context): pass
    
@dev.child
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.option("status", "Status Messsage", type=str, required=True)
@lightbulb.command("setstatus", "Set bot status")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def set_status(ctx: lightbulb.Context):
    await plugin.bot.update_presence(status=hikari.Status.ONLINE, activity=hikari.Activity( name=ctx.options.status, type=hikari.ActivityType.PLAYING,),)
    database.edit_user_data(plugin.bot.get_me().id, "status", ctx.options.status)
    await ctx.respond(notify("presence updated!"))
    
@dev.child
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.option("extension", "Extension", type=str, required=True)
@lightbulb.command("load", "Load an entension")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def load_ext(ctx: lightbulb.Context):
    plugin.bot.load_extensions(f"wolfiebot.{ctx.options.extension}")
    await ctx.respond(notify(f"{ctx.options.extension} loaded"))
    
@dev.child
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.option("extension", "Extension", type=str, required=True)
@lightbulb.command("unload", "Unload an extension")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def unload_ext(ctx: lightbulb.Context):
    plugin.bot.unload_extensions(f"wolfiebot.{ctx.options.extension}")
    await ctx.respond(notify(f"{ctx.options.extension} unloaded"))
    
@dev.child
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.option("extension", "Extension", type=str, required=True)
@lightbulb.command("reload", "Reload an extension")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def reload_ext(ctx: lightbulb.Context):
    plugin.bot.unload_extensions(f"wolfiebot.{ctx.options.extension}")
    plugin.bot.load_extensions(f"wolfiebot.{ctx.options.extension}")
    await ctx.respond(notify(f"{ctx.options.extension} reloaded :arrows_clockwise:"))
    
@dev.child
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.option("toggle", "True/False", type=bool, required=True)
@lightbulb.command("voice", "Turn wolfie voice off")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def voice(ctx: lightbulb.Context):
    database.edit_user_data(plugin.bot.get_me().id, "voice_state", ctx.options.toggle)
    await ctx.respond(notify(f"send voice set to {ctx.options.toggle}"))
    
    
@dev.child
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.option("prompt", "Prompt", type=str, required=True)
@lightbulb.command("prompt", "Change system prompt")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def change_prompt(ctx: lightbulb.Context):
    database.edit_user_data(plugin.bot.get_me().id, "prompt", ctx.options.prompt)
    await ctx.respond(notify(f"prompt changed"))
    
@dev.child
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command("info", "Detailed information")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def info(ctx: lightbulb.Context):
    
    interval = 1
    cpu_percent = psutil.cpu_percent(interval=interval, percpu=True)
    min_cpu_percent = round(min(cpu_percent))
    max_cpu_percent = round(max(cpu_percent))
    avg_cpu_percent = round(sum(cpu_percent) / len(cpu_percent))
    cpu_count = psutil.cpu_count() 

    memory = psutil.virtual_memory()
    total_memory_gb = round(memory.total / (1024 ** 3), 2)
    available_memory_gb = round(memory.available / (1024 ** 3), 2)
    used_memory_gb = round(memory.used / (1024 ** 3), 2)
    memory_percent = memory.percent
    
    os_info = psutil.sys.platform
    boot_time = psutil.boot_time()
    os_uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(boot_time)
    
    memory_format = f"Total: {total_memory_gb}GB\nAvailable: {available_memory_gb}GB\nUsed: {used_memory_gb}GB"
    cpu_format = f"Min: {min_cpu_percent}%\nAVG: {avg_cpu_percent}%\nMax: {max_cpu_percent}%"
    os_format= f"OS: {os_info}\nUptime: {os_uptime}"
    description = f"Memory Usage:\n```{memory_format}```\nCPU Usage:\n ```{cpu_format}```\nOS Info:\n```{os_format}```"
    embed = hikari.Embed(description=description, color=0x000000)
    await ctx.respond(embed)

def notify(message):
    embed = hikari.Embed(title=message, description="", color=0x000000)
    embed.set_author(name=f"Dev Tools", icon=plugin.bot.get_me().display_avatar_url)
    return embed 
    
def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
