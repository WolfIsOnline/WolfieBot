import discord
import wavelink
import logging
import time
import asyncio

from discord.ext import commands
from discord.commands import slash_command
from classes.utils import Utils
from classes._logging import _Logging

RESPONSE_CONNECTED = "I'm in a voice channel"
RESPONSE_DISCONNECTED = "I'm not in a voice channel"
RESPOND_NOT_PLAYING = "I'm not playing anything"
log = _Logging()


class Music(commands.Cog, wavelink.Player):

    def __init__(self, bot):
        self.bot = bot
        self.requester = self.bot
        self.bot.loop.create_task(self.connect_nodes())
        self.bot_util = Utils()

    async def connect_nodes(self):
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(bot=self.bot, host='127.0.0.1', port=2333, password="youshallnotpass")

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node): pass
        #log.info(f"node {node.identifier} is ready on port {node._port}")

    async def display_playing(self, ctx):

        # If you get the vc.position to quickly 
        # it will display the length of the source
        # .5 seconds seems to be the minium amount of time
        # for the vc.position to get the correct position
        await asyncio.sleep(.5)

        vc = ctx.voice_client
        if vc:
            if vc.is_playing():
                embed = discord.Embed(title=f"Now Playing: {vc.source.title}", url=vc.source.uri, color=0x02e7e7)
                embed.set_author(name=f"Uploader: {vc.source.author}")
                embed.set_footer(text=f"Requested By {self.requester}", icon_url=self.requester.display_avatar)
                embed.set_thumbnail(url=vc.source.thumb)

                total = time.strftime("%H:%M:%S", time.gmtime(vc.source.length))
                current = time.strftime("%H:%M:%S", time.gmtime(vc.position))
                embed.add_field(name="Position:", value=f"{current} / {total}", inline=False)
                embed.add_field(name="Source:", value=vc.source.uri, inline=True)

                if vc.source.is_stream():
                    _type = "Live Stream"
                else:
                    _type = "Video"

                embed.add_field(name="Type: ", value=_type, inline=True)
                await ctx.respond(embed=embed)
            else:
                await ctx.respond(RESPOND_NOT_PLAYING)

        else:
            await ctx.respond(RESPONSE_DISCONNECTED)

    @slash_command()
    async def volume(self, ctx, volume: int):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        await player.set_volume(int(volume))
        await ctx.respond("success")

    @slash_command(description="Plays a song.")
    async def play(self, ctx, search: str):
        song = await wavelink.YouTubeTrack.search(query=search, return_first=True)
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client

        await vc.play(song)

        self.requester = ctx.author
        await self.display_playing(ctx)

    @slash_command(description="Shows whats currently playing")
    async def playing(self, ctx):
        await self.display_playing(ctx)

    @slash_command(description="Stops current song.")
    async def stop(self, ctx):
        vc = ctx.voice_client
        if vc:
            if vc.is_playing():
                await vc.stop()
                await ctx.respond("Music stopped")
            else:
                await ctx.respond(ctx, RESPOND_NOT_PLAYING)
        else:
            await ctx.respond(RESPOND_DISCONNECTED)

    @slash_command(description="Disconnects bot from voice channel")
    async def disconnect(self, ctx):
        if not await self.bot_util.is_connected(ctx):
            return await ctx.respond(RESPONSE_DISCONNECTED)
        vc = ctx.voice_client
        await vc.disconnect()
        await ctx.respond("Bye Bye :wave:")

    @slash_command(description="Connects bot to voice channel")
    async def connect(self, ctx):
        await ctx.author.voice.channel.connect(cls=wavelink.Player)
        await ctx.respond("I'm here! :smile:")


def setup(bot):
    bot.add_cog(Music(bot))
