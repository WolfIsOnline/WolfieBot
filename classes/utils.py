import discord

from database.database import Guild_DataBase

gd = Guild_DataBase()
class Utils:
    
    DEFAULT_COLOR = 0x02e7e7

    async def is_connected(self, ctx):
        vc = ctx.voice_client
        if vc:
            return True
        return False

    async def notify(self, ctx, notify_msg):
        embed = discord.Embed(title=None, description=notify_msg, color=self.DEFAULT_COLOR)
        await ctx.respond(embed=embed)

    async def is_owner(self, ctx):
        if ctx.author.id == 257646822925926410:
            return True
        await ctx.respond("You are not the bot owner")
        return False

    async def is_admin(self, ctx):
        if ctx.author.id == int(gd.get_guild_key(ctx.guild.id, "admin_id")):
            return True
        await ctx.respond("You are not an admin")
        return False

    async def is_mod(self, ctx):
        if ctx.author.id == int(gd.get_guild_key(ctx.guild.id, "mod_id")) or ctx.author.id == int(gd.get_guild_key(ctx.guild.id, "admin_id")) or ctx.author.id == 257646822925926410:
            return True
        await ctx.respond("You are not a mod")
        return False