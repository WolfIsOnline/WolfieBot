import wavelink
import discord
import asyncio
import time

from discord.ext import commands
from discord.commands import slash_command
from classes.utils import Utils

MUSIC_PLAYER = "Music | Version: 1.0.0a"
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.requester = self.bot
        self.utils = Utils()
        bot.loop.create_task(self.connect_nodes())

    async def connect_nodes(self):
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(bot=self.bot, host='127.0.0.1', port=2333, password='youshallnotpass',)
        
    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f"Node {node.identifier} is ready on {node.port}")

        
    @slash_command(description="Play a song")
    async def play(self, ctx, search: str):
        
        try:
            song = await wavelink.YouTubeTrack.search(query=search, return_first=True)
        
            if not ctx.voice_client:
                vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player) 
            else:
                vc: wavelink.Player = ctx.voice_client 
            
            await vc.play(song)
            self.requester = ctx.author
            await self.display_playing(ctx, vc)
            
        except AttributeError:
            await self.utils.notify(ctx, "Can't Play", "Join a voice channel to play music", "Music")
        
    
    @slash_command(description="Change music volume")
    async def volume(self, ctx, volume: int):
        if volume > 100:
            volume = 100
        elif volume < 0:
            volume = 0
            
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild) 
        
        await player.set_volume(volume) 
        
        await self.utils.notify(ctx, "Volume Changed", f"Volume set to {volume}", "Music")
        
    async def display_playing(self, ctx, vc):

        # If you get the vc.position to quickly 
        # it will display the length of the source
        # .5 seconds seems to be the minium amount of time
        # for the vc.position to get the correct position
        await asyncio.sleep(.5)
        embed = discord.Embed(title=f"Now Playing: {vc.source.title}", url=vc.source.uri, color=0x02e7e7)
        embed.set_author(name=f"Uploader: {vc.source.author}")
        embed.set_footer(text=f"Requested By {self.requester}", icon_url=self.requester.display_avatar)
        embed.set_thumbnail(url=vc.source.thumb)

        total = time.strftime("%H:%M:%S", time.gmtime(vc.source.length))
        current = time.strftime("%H:%M:%S", time.gmtime(vc.position))
        embed.add_field(name="Position:", value=f"{current} / {total}", inline=False)
        embed.add_field(name="Source:", value=vc.source.uri, inline=True)
        await ctx.respond(embed=embed)
        
        
def setup(bot):
    bot.add_cog(Music(bot))