"""
Dev Commands
"""
import logging
import datetime
import hikari
import lightbulb
import psutil
# pylint: disable=no-name-in-module, import-error, unused-import
import wolfiebot
from wolfiebot.core.bank import Bank
from wolfiebot.database.database import Database
from wolfiebot.ai.api import Api

log = logging.getLogger(__name__)
plugin = lightbulb.Plugin("commands.dev")
database = Database()
api = Api()


@plugin.command
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command("dev", "dev commands")
@lightbulb.implements(lightbulb.PrefixCommandGroup, lightbulb.SlashCommandGroup)
async def dev(ctx: lightbulb.Context):
    """
    Command group for development-related commands.

    This command group is restricted to the bot owner.

    Args:
        ctx (lightbulb.Context): The command invocation context.

    Returns:
        None
    """
    return None

@dev.child
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.option("status", "Status Messsage", type=str, required=True)
@lightbulb.command("setstatus", "Set bot status")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def set_status(ctx: lightbulb.Context):
    """
    Command to set the bot's status.

    This command is restricted to the bot owner
    and requires a status message to be provided as an option.

    Args:
        ctx (lightbulb.Context): The command invocation context.

    Returns:
        None
    """
    await plugin.bot.update_presence(
        status=hikari.Status.ONLINE,
        activity=hikari.Activity(
            name=ctx.options.status,
            type=hikari.ActivityType.PLAYING,
        ),
    )
    database.edit_user_data(plugin.bot.get_me().id,
                            "status", ctx.options.status)
    await ctx.respond(notify("presence updated!"))

@dev.child
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.option("extension", "Extension", type=str, required=True)
@lightbulb.command("load", "Load an entension")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def load_ext(ctx: lightbulb.Context):
    """
    Command to load an extension.

    This command is restricted to the bot owner
    and requires the name of the extension to be provided as an option.

    Args:
        ctx (lightbulb.Context): The command invocation context.

    Returns:
        None
    """
    plugin.bot.load_extensions(f"wolfiebot.{ctx.options.extension}")
    await ctx.respond(notify(f"{ctx.options.extension} loaded"))

@dev.child
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.option("extension", "Extension", type=str, required=True)
@lightbulb.command("unload", "Unload an extension")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def unload_ext(ctx: lightbulb.Context):
    """
    Command to unload an extension.

    This command is restricted to the bot owner
    and requires the name of the extension to be provided as an option.

    Args:
        ctx (lightbulb.Context): The command invocation context.

    Returns:
        None
    """
    plugin.bot.unload_extensions(f"wolfiebot.{ctx.options.extension}")
    await ctx.respond(notify(f"{ctx.options.extension} unloaded"))

@dev.child
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.option("extension", "Extension", type=str, required=True)
@lightbulb.command("reload", "Reload an extension")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def reload_ext(ctx: lightbulb.Context):
    """
    Command to reload an extension.

    This command is restricted to the bot owner
    and requires the name of the extension to be provided as an option.

    Args:
        ctx (lightbulb.Context): The command invocation context.

    Returns:
        None
    """
    plugin.bot.unload_extensions(f"wolfiebot.{ctx.options.extension}")
    plugin.bot.load_extensions(f"wolfiebot.{ctx.options.extension}")
    await ctx.respond(notify(f"{ctx.options.extension} reloaded :arrows_clockwise:"))

@dev.child
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.option("toggle", "True/False", type=bool, required=True)
@lightbulb.command("voice", "Turn wolfie voice off")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def voice(ctx: lightbulb.Context):
    """
    Command to turn off Wolfie voice.

    This command is restricted to the bot owner
    and requires a boolean toggle option (`True` or `False`) to be provided.
    It sets the voice state of the bot to the specified toggle value in the user data.

    Args:
        ctx (lightbulb.Context): The command invocation context.

    Returns:
        None
    """
    database.edit_user_data(plugin.bot.get_me().id,
                            "voice_state", ctx.options.toggle)
    await ctx.respond(notify(f"send voice set to {ctx.options.toggle}"))

@dev.child
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command("info", "Detailed information")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def info(ctx: lightbulb.Context):
    """
    Command to display detailed information about the system.

    This command is restricted to the bot owner.
    It retrieves and displays information about CPU usage, memory usage, and the operating system.
    The information is formatted into an embed and sent as a response.

    Args:
        ctx (lightbulb.Context): The command invocation context.

    Returns:
        None
    """
    cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
    min_cpu_percent = round(min(cpu_percent))
    max_cpu_percent = round(max(cpu_percent))
    avg_cpu_percent = round(sum(cpu_percent) / len(cpu_percent))

    memory = psutil.virtual_memory()
    total_memory_gb = round(memory.total / (1024 ** 3), 2)
    available_memory_gb = round(memory.available / (1024 ** 3), 2)
    used_memory_gb = round(memory.used / (1024 ** 3), 2)

    os_info = psutil.sys.platform
    boot_time = psutil.boot_time()
    os_uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(boot_time)

    memory_format = f"Total: {total_memory_gb}GB\nAvailable: {available_memory_gb}GB\nUsed: {used_memory_gb}GB"
    cpu_format = f"Min: {min_cpu_percent}%\nAVG: {avg_cpu_percent}%\nMax: {max_cpu_percent}%"
    os_format = f"OS: {os_info}\nUptime: {os_uptime}"
    description = f"Memory Usage:\n```{memory_format}```\nCPU Usage:\n ```{cpu_format}```\nOS Info:\n```{os_format}```"
    embed = hikari.Embed(description=description, color=0x000000)
    await ctx.respond(embed)

@dev.child
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.option("level", "level", type=int, required=True)
@lightbulb.option("user", "Select User", type=hikari.User, required=True)
@lightbulb.command("set_level", "Set level multiplier")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def set_level(ctx: lightbulb.Context) -> None:
    """
    Set the level for a user.

    Sets the level of a user to the specified value by adjusting their experience points.
    The required experience points for the specified level are calculated using
    the level multiplier.

    Args:
        ctx (lightbulb.Context): The command invocation context.

    Returns:
        None: The function doesn't return any value.
    """
    level = ctx.options.level
    user = ctx.options.user
    channel_id = ctx.get_channel().id
    # pylint: disable=no-member
    exp_required = await wolfiebot.core.levels.get_exp_required(level)
    await wolfiebot.core.levels.set_exp(user_id=user.id, exp=exp_required, channel_id=channel_id)

def notify(message):
    """
    Creates an embed notification.

    Parameters:
    - message (str): The content of the notification.

    Returns:
    - hikari.Embed: The embed notification.

    This function creates an embed notification with the given message and returns it.
    The embed is styled with a black color and includes the author name set as 'Dev Tools'
    with the bot's display avatar as the icon.
    """
    embed = hikari.Embed(title=message, description="", color=0x000000)
    embed.set_author(
        name="Dev Tools",
        icon=plugin.bot.get_me().display_avatar_url
    )
    return embed


def load(bot: lightbulb.BotApp):
    """
    Loads the plugin into the bot.

    Parameters:
    - bot (lightbulb.BotApp): The bot instance.

    This function adds the plugin to the bot, allowing it to be used and respond to commands.
    """
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp):
    """
    Unloads the plugin from the bot.

    Parameters:
    - bot (lightbulb.BotApp): The bot instance.

    This function removes the plugin from the bot, disabling its functionality and commands.
    """
    bot.remove_plugin(plugin)
