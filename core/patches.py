import discord
import requests

from discord.ext import commands
from classes.utils import Utils
from database.database import GuildDatabase

gd = GuildDatabase()
FREE_GAMES_KEY = "free_games_channel"
GAME_UPDATES_KEY = "game_updates_channel"
PATCH_HOOK_KEY = "patch_hook_channel"

class Patches(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils()

    @commands.Cog.listener()
    async def on_message(self, message):
        guild_id = message.channel.guild.id
        if not message.channel.id == int(gd.get_guild_key(guild_id, PATCH_HOOK_KEY)):
            return
        
        if message.author.id == self.bot.user.id:
            return

        original = message.embeds
        data = None
        for m in original:
            data = m.to_dict()
            
        try:
            if data["title"] == "PatchBot can now notify you of free games" or data["title"] == "Pinned Updates with PatchBot Premium":
                return
            
            title = data["title"]
        except KeyError: title = ""
        
        try:    
            request = requests.get(data["url"], allow_redirects=False)
            request_status_code = request.status_code
            request_headers = request.headers["Location"]
            
        except KeyError: request, request_status_code, request_headers = ""
        
        try: description = data["description"]
        except KeyError: description = ""
        
        try: author = data["author"]["name"]
        except KeyError: author = ""
        
        try: thumbnail = data["thumbnail"]["url"]
        except KeyError: author = ""

        try: image = data["image"]["url"]
        except KeyError: image = ""

        try: fields = data["fields"]
        except KeyError: fields = []

        duplicate = discord.Embed(title=title, description=description, color=self.utils.DEFAULT_COLOR, url=request_headers)
        duplicate.set_author(name=author)
        duplicate.set_thumbnail(url=thumbnail)
        duplicate.set_image(url=image)

        for c in fields:
            duplicate.add_field(name=c["name"], value=c["value"], inline=c["inline"])

        if author == "Epic Games" or author == "Steam" or author == "GOG":
           channel = self.bot.get_channel(int(gd.get_guild_key(guild_id, FREE_GAMES_KEY)))
        else:
           channel = self.bot.get_channel(int(gd.get_guild_key(guild_id, GAME_UPDATES_KEY)))
        await channel.send(embed=duplicate)
        
    async def set_patch_hook(self, ctx, channel: discord.TextChannel):
        gd.update_guild_key(ctx.author.guild.id, PATCH_HOOK_KEY, channel.id)
        
    async def set_free_games(self, ctx, channel: discord.TextChannel):
        gd.update_guild_key(ctx.author.guild.id, FREE_GAMES_KEY, channel.id)
        
    async def set_game_updates(self, ctx, channel: discord.TextChannel):
        gd.update_guild_key(ctx.author.guild.id, GAME_UPDATES_KEY, channel.id)


def setup(bot):
    bot.add_cog(Patches(bot))
