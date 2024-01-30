import hikari
import lightbulb

from wolfiebot.database.database import GuildData
from wolfiebot.ai.simple_api import Simple_API

plugin = lightbulb.Plugin("core.welcome")
simple_api = Simple_API()

SCENE_ID = "workspaces/default-firdbgosgclm_v_vu5dcnw/scenes/discord"
CHARACTER_ID = "-1"


@plugin.listener(hikari.MemberCreateEvent)
async def user_join(event):
    """
    Handles the user join event and sends a welcome message.

    Args:
        event: The event object representing the user join event.

    Returns:
        None
    """
    user = event.user
    user_id = user.id
    guild_id = event.guild_id
    welcome_channel = GuildData(guild_id=guild_id).retrieve(name="welcome_channel")

    session = await simple_api.open_session({user_id: user_id})
    session_id = session.get("name")
    character_id = session.get("sessionCharacters", [])[0].get("character", None)

    response = await simple_api.send_trigger_message(
        session_id=session_id, character_id=character_id, trigger="welcome"
    )

    text_list = response.get("textList")
    combine_text = "".join(text_list)

    await plugin.bot.rest.create_message(
        channel=welcome_channel, content=f"<@{user_id}> {combine_text}"
    )


def load(bot: lightbulb.BotApp):
    """Registers the plugin with the bot instance.

    Args:
        bot: The bot instance to load the plugin into.
    """
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp):
    """Deregisters the plugin from the bot instance.

    Args:
        bot: The bot instance to remove the plugin from.
    """
    bot.remove_plugin(plugin)
