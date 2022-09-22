import wave
import discord
import wavelink
from wavelink.ext import spotify
from wavelink.ext.spotify import SpotifyTrack
import time
import asyncio
from discord.ext import commands
from discord.commands import slash_command

class Music(commands.Cog, wavelink.Player):
    
    def __init__(self, bot):
        self.bot = bot
        self.requester = self.bot

    async def display_playing(self, ctx):
        await asyncio.sleep(.5) # if you don't put the app to sleep it will return the length of the source instead of the current position, this seems to be the min time to sleep
        vc = ctx.voice_client
        if vc:
            if vc.is_playing():
                embed = discord.Embed(title=f"Now Playing: {vc.source.title}", url=vc.source.uri, color=0x02e7e7)
                embed.set_author(name=f"Uploader: {vc.source.author}")
                embed.set_footer(text=f"Requested By {self.requester}", icon_url=self.requester.avatar.url)
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
                await ctx.respond("I'm not playing anything")

        else:
            await ctx.respond("I'm not in a voice channel")

    @slash_command(description="Plays a song.")
    async def play(self, ctx, search: str):
        vc = ctx.voice_client
        if not vc:
            vc = await ctx.author.voice.channel.connect(cls=wavelink.Player)

        if ctx.author.voice.channel.id != vc.channel.id:
            return await ctx.respond("I'm not in your voice channel") 

        song = await wavelink.YouTubeTrack.search(query=search, return_first=True)

        if not song:
            return await ctx.respond("No song was found.")

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
                await ctx.respond("I'm not playing anything")
        else:
            await ctx.respond("I'm not in a voice channel")
            return

def setup(bot):
    bot.add_cog(Music(bot))
