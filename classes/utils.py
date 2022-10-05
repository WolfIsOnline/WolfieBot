import discord

from database.database import GuildDatabase

gd = GuildDatabase()
class Utils:
    
    DEFAULT_COLOR = 0x02e7e7

    async def is_connected(self, ctx):
        vc = ctx.voice_client
        if vc:
            return True
        return False

    async def notify(self, ctx, prompt, info, author, thumbnail="https://images-ext-1.discordapp.net/external/pq6uWSdWFXqOyDcktN0qSBzSkL3Txrk1gEGyoLmeXXE/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1021246946649849867/118da25b10cf765d4472c4664df8dd63.png?width=468&height=468"):
        embed = discord.Embed(title=prompt, description=info, color=self.DEFAULT_COLOR)
        embed.set_thumbnail(url=thumbnail)
        embed.set_author(name=author)
        await ctx.respond(embed=embed)

    async def notify_channel(self, channel, title, message, name):
        embed = discord.Embed(title=title, description=message, color=self.DEFAULT_COLOR)
        embed.set_thumbnail(url=channel.guild.icon.url)
        embed.set_author(name=name)
        await channel.send(embed=embed)


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
