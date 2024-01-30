"""Stat tracking"""
import hikari
import lightbulb

from wolfiebot.database.database import UserData, GuildData

plugin = lightbulb.Plugin("core.stats")


class UserStats:
    def __init__(self, user_id: hikari.Snowflake | int):
        self.user_data = UserData(user_id=user_id)

    def get_messages(self):
        messages = self.user_data.retrieve(name="messages")
        if messages is None:
            messages = 0
        return messages

    def update_messages(self, new_value: int):
        self.user_data.edit(name="messages", value=new_value)


class GuildStats:
    def __init__(self, guild_id: hikari.Snowflake | int):
        self.guild_data = GuildData(guild_id=guild_id)

    def get_messages(self):
        messages = self.guild_data.retrieve(name="messages")
        if messages is None:
            messages = 0
        return messages

    def update_messages(self, new_value: int):
        self.guild_data.edit(name="messages", value=new_value)


@plugin.listener(hikari.GuildMessageCreateEvent)
async def on_message(event):
    if event.is_bot is True or event.message.content.startswith("!"):
        return

    user_stats = UserStats(user_id=event.author.id)
    guild_stats = GuildStats(guild_id=event.guild.id)

    user_messages = user_stats.get_messages()
    guild_messages = guild_stats.get_messages()

    user_stats.update_messages(new_value=user_messages + 1)
    guild_stats.update_messages(new_value=guild_messages + 1)


def load(bot: lightbulb.BotApp) -> None:
    """
    Loads the plugin into the bot.

    Args:
        bot (lightbulb.BotApp): The bot instance.

    Returns:
        None
    """
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    """
    Unloads the plugin from the bot.

    Args:
        bot (lightbulb.BotApp): The bot instance.

    Returns:
        None
    """
    bot.remove_plugin(plugin)
