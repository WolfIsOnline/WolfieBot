from xml.dom import NotFoundErr
import discord

from discord.ext import commands
from discord.ext.commands import context
from discord import SlashCommandGroup
from classes.utils import Utils
from database.database import GuildDatabase
from core.quotes import Quotes
from core.nocturnia import Nocturnia
from core.patches import Patches

gd = GuildDatabase()


class Dev(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils()
        self.quotes = Quotes(bot)
        self.nocturnia = Nocturnia(bot)
        self.patches = Patches(bot)

    dev = SlashCommandGroup("dev", "Dev commands", checks=[commands.is_owner().predicate])

    @dev.command(description="Set admin role")
    async def set_admin(self, ctx, role: discord.Role):
        gd.update_guild_key(ctx.guild.id, "admin_id", role.id)
        await self.utils.notify(ctx, "Admin set", f"Admin set to {role.mention}", "Dev commands")

    @dev.command(description="Set mod role")
    async def set_mod(self, ctx, role: discord.Role):
        gd.update_guild_key(ctx.guild.id, "mod_id", role.id)
        await self.utils.notify(ctx, "Mod set", f"Mod set to {role.mention}", "Dev commands")

    @dev.command(description="kills person")
    async def kill(self, ctx, user: discord.User):
        await self.nocturnia.notify_death(user.id)
        await self.utils.notify(ctx, "User killed", f"{user} has been killed", "Dev commands")

    @dev.command(description="reload cog")
    async def reload(self, ctx, cog):
        self.bot.reload_extension(f"core.{cog}")
        await self.utils.notify(ctx, "Reloaded", f"{cog} successfully reloaded", "Dev commands")

    @dev.command(description="load cog")
    async def load(self, ctx, cog):
        self.bot.load_extension(f"core.{cog}")
        await self.utils.notify(ctx, "Loaded", f"{cog} successfully loaded", "Dev commands")

    @dev.command(description="unload cog")
    async def unload(self, ctx, cog):
        self.bot.unload_extension(f"core.{cog}")
        await self.utils.notify(ctx, "Unloaded", f"{cog} successfully unloaded", "Dev commands")
        
    @dev.command(description="set patches hook")
    async def set_patch_hook(self, ctx, channel: discord.TextChannel):
        await self.patches.set_patch_hook(ctx, channel)
        await self.utils.notify(ctx, "Patch Hook Set", f"Patch hook set to {channel.mention}", "Dev commands")

    @dev.command(description="set patches hook")
    async def set_game_updates(self, ctx, channel: discord.TextChannel):
        await self.patches.set_game_updates(ctx, channel)
        await self.utils.notify(ctx, "Game Updates Set", f"Game updates set to {channel.mention}", "Dev commands")
        
    @dev.command(description="set patches hook")
    async def set_free_games(self, ctx, channel: discord.TextChannel):
        await self.patches.set_free_games(ctx, channel)
        await self.utils.notify(ctx, "Free Games Set", f"Free games set to {channel.mention}", "Dev commands")

def setup(bot):
    bot.add_cog(Dev(bot))
