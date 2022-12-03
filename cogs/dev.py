from xml.dom import NotFoundErr
import discord

from discord.ext import commands, bridge
from discord.ext.commands import context
from discord import SlashCommandGroup
from classes.utils import Utils
from database.database import GuildDatabase
from cogs.quotes import Quotes
from cogs.nocturnia import Nocturnia
from cogs.patches import Patches
from cogs.economy import Economy
from cogs.info import Info
from discord.ext.pages import Paginator, Page


gd = GuildDatabase()


class Dev(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils()
        self.quotes = Quotes(bot)
        self.nocturnia = Nocturnia(bot)
        self.patches = Patches(bot)
        self.economy = Economy(bot)
        self.info = Info(bot)

    @bridge.bridge_group()
    async def dev(self, ctx): pass
        
    @dev.command(description="kills person")
    async def kill(self, ctx, user: discord.User):
        if await self.utils.is_dev(ctx) is False: return
        await self.nocturnia.notify_death(user.id)
        await self.utils.notify(ctx, "User killed", f"{user} has been killed", "Dev commands")

    @dev.command(description="reload cog")
    async def reload(self, ctx, cog):
        if await self.utils.is_dev(ctx) is False: return
        self.bot.reload_extension(f"core.{cog}")
        await self.utils.notify(ctx, "Reloaded", f"{cog} successfully reloaded", "Dev commands")

    @dev.command(description="load cog")
    async def load(self, ctx, cog):
        if await self.utils.is_dev(ctx) is False: return
        self.bot.load_extension(f"core.{cog}")
        await self.utils.notify(ctx, "Loaded", f"{cog} successfully loaded", "Dev commands")

    @dev.command(description="unload cog")
    async def unload(self, ctx, cog):
        if await self.utils.is_dev(ctx) is False: return
        self.bot.unload_extension(f"core.{cog}")
        await self.utils.notify(ctx, "Unloaded", f"{cog} successfully unloaded", "Dev commands")
        
    @dev.command(description="set patches hook")
    async def set_patch_hook(self, ctx, channel: discord.TextChannel):
        if await self.utils.is_dev(ctx) is False: return
        await self.patches.set_patch_hook(ctx, channel)
        await self.utils.notify(ctx, "Patch Hook Set", f"Patch hook set to {channel.mention}", "Dev commands")

    @dev.command(description="set patches hook")
    async def set_game_updates(self, ctx, channel: discord.TextChannel):
        if await self.utils.is_dev(ctx) is False: return
        await self.patches.set_game_updates(ctx, channel)
        await self.utils.notify(ctx, "Game Updates Set", f"Game updates set to {channel.mention}", "Dev commands")
        
    @dev.command(description="set patches hook")
    async def set_free_games(self, ctx, channel: discord.TextChannel):
        if await self.utils.is_dev(ctx) is False: return
        await self.patches.set_free_games(ctx, channel)
        await self.utils.notify(ctx, "Free Games Set", f"Free games set to {channel.mention}", "Dev commands")

    @dev.command(description="Give user money")
    async def give_money(self, ctx, amount: int, user: discord.User):
        if await self.utils.is_dev(ctx) is False: return
        await self.economy.give_money(ctx, amount, user)
        await self.utils.notify(ctx, "Money Given", f"§{amount:,} has been given to {user}", "Dev commands")

    @dev.command(description="Take user money")
    async def take_money(self, ctx, amount: int, user: discord.User):
        if await self.utils.is_dev(ctx) is False: return
        await self.economy.take_money(ctx, amount, user)
        await self.utils.notify(ctx, "Money Taken", f"§{amount:,} has been taken from {user}", "Dev commands")
        
    @dev.command()
    async def check(self, ctx):
        if await self.utils.is_dev(ctx) is False: return
        await ctx.respond(f"{ctx.author.mention}")
        
    @dev.command()
    async def displayembed(self, ctx):
        message = await ctx.fetch_message(1032671702926229554)
        for embed in message.embeds:
            await ctx.respond(embed.to_dict())
            
    @dev.command()
    async def push_changelog(self, ctx):
        with open("changelog.txt", "r") as log:
            changes = log.read()
        embed = discord.Embed(title=f"Updated to {self.info.BOT_VERSION}", description=changes, color=self.utils.DEFAULT_COLOR)
        embed.set_footer(text="Wolfie is now in 5 servers")
        channel_id = gd.get_guild_key(ctx.author.guild.id, "modlog_channel")
        channel = ctx.author.guild.get_channel(int(channel_id))
        await channel.send(embed=embed)
        await ctx.respond("pushed!", ephemeral=True)
        

def setup(bot):
    bot.add_cog(Dev(bot))
