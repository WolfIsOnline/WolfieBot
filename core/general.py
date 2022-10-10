import discord

from discord.ext import commands
from discord.commands import slash_command
from discord import SlashCommandGroup
from classes.utils import Utils
from core.nocturnia import Nocturnia
from core.economy import Economy


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils()
        self.nocturnia = Nocturnia(bot)
        self.economy = Economy(bot)

    math = SlashCommandGroup("math", "Math commands")

    @math.command(description="Add two numbers")
    async def add(self, ctx, num1: float, num2: float):
        return await ctx.respond(f"{num1 + num2}")

    @math.command(description="Subtract two numbers")
    async def subtract(self, ctx, num1: float, num2: float):
        return await ctx.respond(f"{num1 - num2}")

    @math.command(description="Multiply two numbers")
    async def multiply(self, ctx, num1: float, num2: float):
        return await ctx.respond(f"{num1 * num2}")

    @math.command(description="Divide two numbers")
    async def divide(self, ctx, num1: float, num2: float):
        if num2 == 0:
            await self.nocturnia.notify_death(ctx.author.id)
            return await ctx.respond("What have you done?")
        return await ctx.respond(f"{num1 / num2}")

    @slash_command(description="Get users profile picture")
    async def pfp(self, ctx, user: discord.User):
        avatar = discord.Embed(color=self.utils.DEFAULT_COLOR)
        avatar.set_image(url=user.display_avatar)
        await ctx.respond(embed=avatar)

    @slash_command(description="Pong")
    async def ping(self, ctx):
        await ctx.respond("Pong")
        
    @slash_command(description="Transfer funds to another member")
    async def transfer(self, ctx, amount : int, user: discord.User):
        await self.economy.transfer(ctx, amount, ctx.author, user)


def setup(bot):
    bot.add_cog(General(bot))
