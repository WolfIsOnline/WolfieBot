import discord

from discord.ext import commands
from discord.commands import slash_command
from discord import SlashCommandGroup
from core.automove import AutoMove
from core.modlogs import ModLogs
from core.welcome import Welcome
from core.economy import Economy
from core.quotes import Quotes
from classes.utils import Utils
from database.database import GuildDatabase

gd = GuildDatabase()
class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.auto_move = AutoMove(bot)
        self.mod_logs = ModLogs(bot)
        self.welcome = Welcome(bot)
        self.quotes = Quotes(bot)
        self.economy = Economy(bot)
        self.utils = Utils()

    admin = SlashCommandGroup("admin", "Admin commands")

    @admin.command(description="Sets auto room")
    async def set_auto_room(self, ctx, channel: discord.VoiceChannel):
        await self.auto_move.set_auto_room(ctx, channel.id)
        await self.utils.notify(ctx, "Auto Room", f"Auto Room is now set to {channel.mention}", "Admin commands")

    @admin.command(description="Give user money")
    async def give_money(self, ctx, amount: int, user: discord.User):
        await self.economy.give_money(ctx, amount, user)
        await self.utils.notify(ctx, "Money Given", f"§{amount:,} has been given to {user}", "Admin commands")

    @admin.command(description="Take user money")
    async def take_money(self, ctx, amount: int, user: discord.User):
        await self.economy.take_money(ctx, amount, user)
        await self.utils.notify(ctx, "Money Taken", f"§{amount:,} has been taken from {user}", "Admin commands")

    @admin.command(description="Set modlog to specified channel")
    async def set_mod_log(self, ctx, channel: discord.TextChannel):
        await self.mod_logs.set_mod_log(ctx, channel.id)
        await self.utils.notify(ctx, "Mod logs set", f"Mod logs will now display in {channel.mention}", "Admin commands")

    @admin.command(description="Set welcome channel")
    async def set_welcome(self, ctx, channel: discord.TextChannel):
        await self.welcome.set_welcome(ctx, channel.id)

    @admin.command(description="Update quote file")
    async def force_update(self, ctx):
        await self.quotes.force_refresh(ctx.author.guild.id)
        await ctx.respond("Log file updated")

    @admin.command(description="Set quotes channel")
    async def set_quotes(self, ctx, channel: discord.TextChannel):
        guild_id = ctx.author.guild.id
        await self.quotes.set_quotes(guild_id, channel.id)
        await ctx.respond(f"Quotes channel set to {channel.mention}")
        
    @admin.command(description="Add quote by ID")
    async def add_quote(self, ctx, message_id):
        guild_id = ctx.author.guild.id
        channel = self.bot.get_channel(gd.get_guild_key(guild_id, "quotes_channel"))
        message = await channel.fetch_message(int(message_id))
        await self.quotes.add_quote(guild_id, message)
        await ctx.respond("Done", ephemeral=True)


def setup(bot):
    bot.add_cog(AdminCommands(bot))
