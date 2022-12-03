import discord

from discord.ext import commands, bridge
from discord.commands import slash_command
from discord import SlashCommandGroup
from cogs.automove import AutoMove
from cogs.modlogs import ModLogs
from cogs.welcome import Welcome
from cogs.economy import Economy
from cogs.quotes import Quotes
from cogs.autorole import AutoRole
from cogs.simpleembed import SimpleEmbed
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
        self.auto_role = AutoRole(bot)
        self.simple_embed = SimpleEmbed(bot)

    @bridge.bridge_group()
    async def admin(self, ctx): pass

    @admin.command(description="Sets auto room")
    async def set_auto_room(self, ctx, channel: discord.VoiceChannel):
        if await self.utils.is_admin(ctx) is not True:
            return
        
        await self.auto_move.set_auto_room(ctx, channel.id)
        await self.utils.notify(ctx, "Auto Room", f"Auto Room is now set to {channel.mention}", "Admin commands")

    @admin.command(description="Set modlog to specified channel")
    async def set_mod_log(self, ctx, channel: discord.TextChannel):
        if await self.utils.is_admin(ctx) is not True:
            return
        
        await self.mod_logs.set_mod_log(ctx, channel.id)
        await self.utils.notify(ctx, "Mod logs set", f"Mod logs will now display in {channel.mention}", "Admin commands")

    @admin.command(description="Set welcome channel")
    async def set_welcome(self, ctx, channel: discord.TextChannel):
        if await self.utils.is_admin(ctx) is not True:
            return
        
        await self.welcome.set_welcome(ctx, channel.id)

    @admin.command(description="Update quote file")
    async def force_update(self, ctx):
        if await self.utils.is_admin(ctx) is not True:
            return
        
        await self.quotes.force_refresh(ctx.author.guild.id)
        await ctx.respond("Log file updated")

    @admin.command(description="Set quotes channel")
    async def set_quotes(self, ctx, channel: discord.TextChannel):
        if await self.utils.is_admin(ctx) is not True:
            return
        
        guild_id = ctx.author.guild.id
        await self.quotes.set_quotes(guild_id, channel.id)
        await ctx.respond(f"Quotes channel set to {channel.mention}")
        
    @admin.command(description="Add quote by ID")
    async def add_quote(self, ctx, message_id):
        if await self.utils.is_admin(ctx) is not True:
            return
        
        guild_id = ctx.author.guild.id
        channel = self.bot.get_channel(int(gd.get_guild_key(guild_id, "quotes_channel")))
        message = await channel.fetch_message(int(message_id))
        await self.quotes.add_quote(guild_id, message)
        await ctx.respond("Done", ephemeral=True)
        
    @admin.command(description="Add auto role to list")
    async def add_auto_role(self, ctx, role: discord.Role):
        if await self.utils.is_admin(ctx) is not True:
            return
        
        await self.auto_role.add_auto_role(role)
        await ctx.respond("role added")
        
    @admin.command(description="Purge channel")
    async def purge(self, ctx, amount = 1):
        if await self.utils.is_admin(ctx) is not True:
            return
        
        await ctx.channel.purge(limit=int(amount))
        await ctx.respond(str(amount) + " messages have been deleted!", delete_after=3)
    
    @admin.command(description="Set mod role")
    async def set_mod(self, ctx, role: discord.Role):
        if await self.utils.is_admin(ctx) is not True:
            return
        
        gd.update_guild_key(ctx.guild.id, "mod_id", role.id)
        await self.utils.notify(ctx, "Mod set", f"Mod set to {role.mention}", "Admin commands")
        
    @admin.command(description="Display admin dashboard")
    async def dashboard(self, ctx):
        if await self.utils.is_admin(ctx) is not True:
            return
        
        guild_id = ctx.guild.id
        embed = discord.Embed(title="Admin Dashboard", description="", color=self.utils.DEFAULT_COLOR)
        try:
            channel_id = int(gd.get_guild_key(guild_id, "modlog_channel"))
            channel = self.bot.get_channel(channel_id)
            embed.add_field(name="Modlog Channel: ", value=channel.mention)
        except ValueError:
            embed.add_field(name="Modlog Channel: ", value="Not set")
        except AttributeError: pass
        
        try:
            channel_id = int(gd.get_guild_key(guild_id, "automove_source"))
            channel = self.bot.get_channel(channel_id)
            embed.add_field(name="Autoroom Channel: ", value=channel.mention)
        except ValueError: embed.add_field(name="Autoroom Channel: ", value="Not set")
        except AttributeError: pass
            
        try:
            role_id = int(gd.get_guild_key(guild_id, "mod_id"))
            role = ctx.guild.get_role(role_id)
            embed.add_field(name="Mod Role: ", value=role.mention)
        except ValueError:
            embed.add_field(name="Mod Role: ", value="Not set")
        except AttributeError: pass
            
        try:
            channel_id = int(gd.get_guild_key(guild_id, "welcome_channel"))
            channel = self.bot.get_channel(channel_id)
            embed.add_field(name="Welcome Channel: ", value=channel.mention)
        except ValueError:
            embed.add_field(name="Welcome Channel: ", value="Not set")
        except AttributeError: pass
            
        try:
            role = []
            role_ids = gd.get_guild_key_array(guild_id, "autoroles")

            for c in role_ids:
                role_name = ctx.guild.get_role(c)
                role.append(role_name.mention)
            
            embed.add_field(name="Auto Roles: ", value=role)
        except ValueError:
            embed.add_field(name="Auto Roles: ", value="None set")
        except AttributeError: pass

        await ctx.respond(embed=embed)
        
    @admin.command(description="Display admin dashboard")
    async def embed(self, ctx, channel: discord.TextChannel):
        if await self.utils.is_admin(ctx) is not True:
            return
        
        await self.simple_embed.simple_embed(ctx, channel)


def setup(bot):
    bot.add_cog(AdminCommands(bot))
