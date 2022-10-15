import discord

from database.database import GuildDatabase

gd = GuildDatabase()
NO_ACCESS = "You do not have access to this command"
THUMBNAIL = "https://images-ext-1.discordapp.net/external/pq6uWSdWFXqOyDcktN0qSBzSkL3Txrk1gEGyoLmeXXE/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1021246946649849867/118da25b10cf765d4472c4664df8dd63.png?width=468&height=468"
class Utils:
    
    DEFAULT_COLOR = 0x02e7e7

    async def is_connected(self, ctx):
        vc = ctx.voice_client
        if vc:
            return True
        return False

    async def notify(self, ctx, prompt, info, author, thumbnail=THUMBNAIL):
        embed = discord.Embed(title=prompt, description=info, color=self.DEFAULT_COLOR)
        embed.set_thumbnail(url=thumbnail)
        embed.set_author(name=author)
        await ctx.respond(embed=embed)

    async def notify_channel(self, channel, prompt, info, author, thumbnail=THUMBNAIL):
        embed = discord.Embed(title=prompt, description=info, color=self.DEFAULT_COLOR)
        embed.set_thumbnail(url=thumbnail)
        embed.set_author(name=author)
        await channel.send(embed=embed)


    async def is_dev(self, ctx):
        if ctx.author.id == 257646822925926410:
            return True
        await ctx.respond(NO_ACCESS)
        return False
        
    async def is_owner(self, ctx):
        if ctx.author.id == ctx.guild.owner.id or ctx.author.id == 257646822925926410:
            return True
        await ctx.respond(NO_ACCESS)
        return False

    async def is_admin(self, ctx):
        if ctx.author.id == int(gd.get_guild_key(ctx.guild.id, "admin_id")) or ctx.author.id == ctx.guild.owner.id:
            return True
        await ctx.respond(NO_ACCESS)
        return False

    async def is_mod(self, ctx):
        if ctx.author.id == int(gd.get_guild_key(ctx.guild.id, "mod_id")) or ctx.author.id == int(gd.get_guild_key(ctx.guild.id, "admin_id")) or ctx.author.id == 257646822925926410:
            return True
        await ctx.respond(NO_ACCESS)
        return False
