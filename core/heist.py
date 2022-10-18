import math
import discord
import asyncio
import random

from discord.ext import commands, bridge
from discord.commands import slash_command
from database.database import GuildDatabase
from classes.utils import Utils
from classes.transactions import Transactions
from core.nocturnia import Nocturnia

gd = GuildDatabase()


class Heist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils()
        self.nocturnia = Nocturnia(bot)
        self.game = "heist"
        self.chance = 5
        self.transactions = Transactions()
        self.players = []
        self.dead = []
        self.alive = []

    @commands.cooldown(1, 3600, commands.BucketType.user)
    @bridge.bridge_command(description="Rob someone")
    async def heist(self, ctx, user: discord.User):

        player_id = ctx.author.id
        guild_id = ctx.author.guild.id
        target_id = user.id

        running = gd.get_guild_key(guild_id, "heist_running")
        if running == "None":
            running = False
            print("nothing is running, starting game")
        else:
            running = bool(gd.get_guild_key(guild_id, "heist_running"))
        if running is True:
            return await self.utils.notify(ctx, "Can't Join", "A heist has already been started", "Heist")

        if player_id == target_id:
            return await self.utils.notify(ctx, "Can't Start", "You can't start a heist on yourself", "Heist")

        print(f"heist has started in {guild_id}")
        start_cost = 10000
        target_limit = 5000

        leader_balance = self.transactions.get_balance(player_id)
        if leader_balance < start_cost:
            return await self.utils.notify(ctx, "Can't Start",
                                           f"You need at least {start_cost:,} Eurodollar's to start a heist", "Heist")

        target_balance = self.transactions.get_balance(target_id)
        if target_balance < target_limit:
            return await self.utils.notify(ctx, "Can't Start", f"{user} has less than {target_limit:,} Eurodollar's",
                                           "Heist")

        gd.update_guild_key(guild_id, "heist_running", True)
        gd.update_guild_key(guild_id, "heist_can_join", True)
        gd.update_guild_key(guild_id, "heist_target", target_id)
        self.players.append(player_id)

        screen = discord.Embed(title="Heist Started",
                               description=f"{ctx.author.mention} has started a heist targeting {user.mention} /joinheist to join in",
                               color=self.utils.DEFAULT_COLOR)
        screen.set_thumbnail(
            url="https://images-ext-1.discordapp.net/external/pq6uWSdWFXqOyDcktN0qSBzSkL3Txrk1gEGyoLmeXXE/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1021246946649849867/118da25b10cf765d4472c4664df8dd63.png?width=468&height=468")
        screen.set_author(name="Heist")
        screen.set_footer(text=f"Success Chance: {self.chance}%")
        self.start_screen = await ctx.respond(embed=screen)

        await self.transactions.withdraw(ctx.author.id, start_cost, "heist startup costs", "anonymous")

        await asyncio.sleep(20)
        gd.update_guild_key(guild_id, "heist_can_join", False)

        for index in range(len(self.players)):
            player = self.players[index]
            death = self.decide(5)
            if death[0] is True: self.dead.append(player)
            if death[0] is False: self.alive.append(player)

        player_left = len(self.alive)
        if player_left == 0:
            await self.end_heist(ctx, target_id)
            return await ctx.send("Everyone has died, the heist has failed.")

        if self.chance > 75:
            self.chance = 75
        success = self.decide(self.chance)
        print(f"Success: {success}")

        stolen_amount_percentage = random.randrange(10, 35)
        stole_amount = self.get_stolen_amount(target_balance, stolen_amount_percentage)
        split = stole_amount / player_left
        split = int(split)

        if success[0] is False:
            await self.end_heist(ctx, target_id)
            return await self.utils.notify(ctx, "Heist FAILED",
                                           f"The heist has failed, all startup and contribution costs have been lost",
                                           "Heist")

        await self.utils.notify(ctx, "Heist SUCCESSFUL",
                                f"The heist was a success. **§{stole_amount:,} ({stolen_amount_percentage}% total balance)** was stolen",
                                "Heist")
        await asyncio.sleep(1)

        for c in self.players:
            if self.get_dead(c) is True:
                await ctx.send(f"<@{c}> has died")
                await self.nocturnia.notify_death(c)

            elif self.get_dead(c) is False:
                await ctx.send(f"<@{c}> recieved §{split:,}")
                await self.transactions.deposit(c, split, "heist cut", "anonymous")
            await asyncio.sleep(.5)

        await self.transactions.withdraw(user.id, stole_amount, "robbed", "heisters")

        await self.end_heist(ctx, target_id)

    async def end_heist(self, ctx, target_id):
        self.players.clear()
        self.alive.clear()
        self.dead.clear()
        gd.delete_guild_key(ctx.author.guild.id, "heist_running", True)
        gd.delete_guild_key(ctx.author.guild.id, "heist_can_join", False)
        gd.delete_guild_key(ctx.author.guild.id, "heist_target", target_id)
        self.chance = 5
        print(f"heist has ended on {ctx.author.guild.id}")

    def get_stolen_amount(self, amount, percentage):
        return int(amount * percentage / 100)

    def get_dead(self, player):
        for _player in self.dead:
            if _player == player:
                return True
        return False

    def decide(self, percentage: int):
        rand = random.randint(1, 100)
        if rand <= percentage:
            return [True, f"{rand}%"]
        else:
            return [False, f"{rand}%"]

    @bridge.bridge_command(description="Join a heist")
    async def join_heist(self, ctx):
        player_id = ctx.author.id

        check = await self.check_join(ctx.author.guild.id, player_id)

        if check[0] is False:
            return await self.utils.notify(ctx, "Can't Join", check[1], "Heist")

        cost = 2000

        player_balance = self.transactions.get_balance(player_id)
        if player_balance < cost:
            return await self.utils.notify(ctx, "Can't Join",
                                           f"You need at least {cost:,} Eurodollar's to join the heist", "Heist")

        self.players.append(player_id)
        await self.transactions.withdraw(player_id, cost, "heist contribution", "anonymous")

        self.chance += 10
        await ctx.respond(f"{ctx.author.mention} has joined (Chance of success **{self.chance}%**)")

    async def check_join(self, guild_id, player_id):

        target = gd.get_guild_key(guild_id, "heist_target")
        if target == "None":
            target = 0
        else:
            target = int(gd.get_guild_key(guild_id, "heist_target"))
        print(target)
        can_join = gd.get_guild_key(guild_id, "heist_can_join")
        if can_join == "None":
            can_join = False
        else:
            can_join = bool(gd.get_guild_key(guild_id, "heist_can_join"))

        if can_join is False:
            reason = "There is an ongoing heist"
            check = False
            return [check, reason]

        elif target == player_id:
            reason = "You cannot join a heist against yourself"
            check = False
            return [check, reason]

        for player in self.players:
            if player_id == player:
                reason = "You are already in the heist"
                check = False
                return [check, reason]
        return [True, None]


def setup(bot):
    bot.add_cog(Heist(bot))
