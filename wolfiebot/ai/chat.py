"""
AI Listeners
"""
import logging
import hikari
import lightbulb
import re
import time
import asyncio

from wolfiebot.ai.chat_manager import AIManager
plugin = lightbulb.Plugin("ai.chat")
log = logging.getLogger(__name__)

@plugin.listener(hikari.GuildMessageCreateEvent)
async def guild_listen(event) -> None:
    if event.author_id == plugin.bot.get_me().id:
        return
    
    if plugin.bot.get_me().id in event.message.user_mentions:
        user = plugin.bot.cache.get_member(event.guild_id, event.author.id)
        name = user.nickname
        if name is None:
            name = user
        await chat(event)

@plugin.listener(hikari.DMMessageCreateEvent)
async def direct_listen(event) -> None:
    if event.author_id == plugin.bot.get_me().id:
        return

    await chat(event)

async def chat(event) -> None:
    message = re.sub(r"<.*?>", "", event.message.content)
    manager = AIManager(event.author.id)
    async with plugin.bot.rest.trigger_typing(event.channel_id):
        reply = await manager.send_message(message)

    if reply is None:
        return

    await event.app.rest.create_message(
        channel=event.channel_id,
        content=reply,
        reply=event.message
    )

def load(bot: lightbulb.BotApp) -> None:
    """
    Loads the plugin into the specified bot.

    Args:
        bot (lightbulb.BotApp): The bot instance to load the plugin into.
    """
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    """
    Unloads the plugin from the specified bot.

    Args:
        bot (lightbulb.BotApp): The bot instance to unload the plugin from.
    """
    bot.remove_plugin(plugin)
