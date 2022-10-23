from dis import dis
from sqlite3 import connect
import wavelink
import discord
import asyncio
import time

from wavelink.player import Player
from discord.ext import commands, bridge
from discord.commands import slash_command
from classes.utils import Utils

COG = "Music"
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
    
    @bridge.bridge_command(description="Disconnect bot")
    async def disconnect(self, ctx):
        try:
            player = self.get_node_player(ctx)
            await player.disconnect()
            await ctx.respond("Bye bye! :wave:")
        except AttributeError:
            pass
        
    @bridge.bridge_command(description="Stops and clears queue")
    async def stop(self, ctx):
        player = self.get_node_player(ctx)
        try:
            await player.stop()
            await self.utils.notify(ctx, "Stopped", "Player has stopped", COG)
            
        except AttributeError:
            pass     
        
    @bridge.bridge_command(description="Pause current song")
    async def pause(self, ctx):
        try:
            player = self.get_node_player(ctx)
            await player.pause()
            await self.display_playing(ctx, player)
            
        except AttributeError:
            pass
        
    @bridge.bridge_command(description="Resume current song")
    async def resume(self, ctx):
        try:
            player = self.get_node_player(ctx)
            await player.resume()
            await self.display_playing(ctx, player)
        
        except AttributeError:
            pass
    
    @bridge.bridge_command(description="Play a song")
    async def play(self, ctx, song: str):
        player = self.get_node_player(ctx)
        try:
            user_voice_channel = ctx.author.voice.channel
            if player is None:
                player = await user_voice_channel.connect(cls=wavelink.Player)
                
        except AttributeError:
            return await self.utils.notify(ctx, "Can't Play", "You are not in a voice channel", COG)
        
        track = await wavelink.YouTubeTrack.search(query=song, return_first=True)
        await player.play(track)
        self.requester = ctx.author
        await self.display_playing(ctx, player)
        
    @bridge.bridge_command(description="Display whats playing")
    async def playing(self, ctx):
        player = self.get_node_player(ctx)
        await self.display_playing(ctx, player)

    @bridge.bridge_command(description="Change music volume")
    async def volume(self, ctx, volume: int):
        if volume > 100:
            volume = 100
        elif volume < 0:
            volume = 0
            
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild) 
        
        await player.set_volume(volume) 
        
        await self.utils.notify(ctx, "Volume Changed", f"Volume set to {volume}", COG)
        
    
    def get_node_player(self, ctx):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild) 
        return player  
    
    async def display_playing(self, ctx, player):

        # If you get the vc.position to quickly 
        # it will display the length of the source
        # .5 seconds seems to be the minium amount of time
        # for the vc.position to get the correct position
        await asyncio.sleep(.5)
        if player.is_paused():
            embed = discord.Embed(title=f"Paused: {player.source.title}", url=player.source.uri, color=0x02e7e7)
        else:
            embed = discord.Embed(title=f"Playing: {player.source.title}", url=player.source.uri, color=0x02e7e7)
        embed.set_author(name=f"Uploader: {player.source.author}")
        embed.set_footer(text=f"Requested By {self.requester}", icon_url=self.requester.display_avatar)
        embed.set_thumbnail(url=player.source.thumb)

        total = time.strftime("%H:%M:%S", time.gmtime(player.source.length))
        current = time.strftime("%H:%M:%S", time.gmtime(player.position))
        embed.add_field(name="Position:", value=f"{current} / {total}", inline=False)
        embed.add_field(name="Source:", value=player.source.uri, inline=True)
        await ctx.respond(embed=embed)
        
        
def setup(bot):
    bot.add_cog(Music(bot))