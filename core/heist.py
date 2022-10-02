import math
import discord
import asyncio
import random

from discord.ext import commands
from discord.commands import slash_command
from classes.utils import Utils
from classes.transactions import Transactions
from core.nocturnia import Nocturnia

class Heist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils()
        self.nocturnia = Nocturnia(bot)
        self.chance = 5
        self.target = 0
        self.canJoin = False
        self.started = False
        self.leader = None
        self.transactions = Transactions()
        self.players = []
        self.dead = []
        self.alive = []

    @slash_command(description="Rob someone")
    async def heist(self, ctx, user: discord.User):
        if self.started == True: return await self.utils.notify(ctx, "Can't Join", "A heist has already been started", "Heist")
        if ctx.author.id == user.id: return await self.utils.notify(ctx, "Can't Start", "You can't start a heist on yourself", "Heist")
        
        start_cost = 10000
        target_limit = 5000
        leader_balance = self.transactions.get_balance(ctx.author.id)
        if(leader_balance < start_cost): return await self.utils.notify(ctx, "Can't Start", f"You need at least {start_cost:,} Eurodollar's to start a heist", "Heist")

        target_balance = self.transactions.get_balance(user.id)
        if(target_balance < target_limit): return await self.utils.notify(ctx, "Can't Start", f"{user} has less than {target_limit:,} Eurodollar's", "Heist")

        self.target = user.id
        self.canJoin = True
        self.started = True
        self.leader = ctx.author.id
        self.players.append(self.leader)
        
        await self.utils.notify(ctx, "Heist Started!", f"{ctx.author.mention} has started a heist targeting {user.mention} /joinheist to join in", "Heist")

        await asyncio.sleep(20)
        await self.transactions.withdraw(ctx.author.id, start_cost, "heist startup costs", "anonymous")

        for index in range(len(self.players)):
            player = self.players[index]
            death = self.decide(5)
            if death[0] == True: self.dead.append(player)
            if death[0] == False: self.alive.append(player)
            print(f"{player} : {death}")

        player_left = len(self.alive)
        if player_left == 0:
            await self.endheist(ctx)
            return await ctx.send("Everyone has died, the heist has failed.")
        
        if self.chance > 75:
            self.chance = 75
        success = self.decide(self.chance)
        print(f"Success: {success}")

        stolen_amount_percentage = random.randrange(10, 35)
        stole_amount = self.get_stolen_amount(target_balance, stolen_amount_percentage)
        split = stole_amount / player_left
        split = int(split)

        if(success[0] == False):
            await self.endheist(ctx)
            return await self.utils.notify(ctx, "Heist FAILED", f"This heist was not successful, all startup cost and contribution cost have been lost", "Heist")

        await self.utils.notify(ctx, "Heist SUCCESSFUL", f"The heist was a success. **{stole_amount:,} ({stolen_amount_percentage}% total balance)** was stolen", "Heist")
        await asyncio.sleep(2)

        for c in self.players:
            if self.getdead(c) == True:
                await ctx.send(f"<@{c}> has died")
                await self.nocturnia.notify_death(c)

            elif self.getdead(c) == False:
                await ctx.send(f"<@{c}> recieved §{split:,}")
                await self.transactions.deposit(c, split, "heist cut", "anonymous")
            await asyncio.sleep(.5)
        
        await self.transactions.withdraw(user.id, stole_amount, "robbed", "heisters")

        await self.endheist(ctx)



    async def endheist(self, ctx):
        self.players.clear()
        self.alive.clear()
        self.dead.clear()
        self.target = 0
        self.chance = 5
        self.started = False
        self.canJoin = False

    def get_stolen_amount(self, amount, percentage):
        return int(amount * percentage / 100)

    def getdead(self, player):
        for _player in self.dead:
            if _player == player:
                return True
        return False

    def decide(self, percentage : int):
        rand = random.randint(1, 100)
        if rand <= percentage: return [True, f"{rand}%"]
        else: return [False, f"{rand}%"]
            

    @slash_command(description="Join a heist")
    async def joinheist(self, ctx):
        if self.canJoin == False:
            return await self.utils.notify(ctx, "Can't Join", "There is no ongoing heist", "Heist")
        
        if self.target == ctx.author.id:
            return await self.utils.notify(ctx, "Can't Join", "You can't join a heist against you", "Heist")

        for c in self.players:
            if ctx.author.id == c:
                return await self.utils.notify(ctx, "Can't Join", "You are already in this heist", "Heist")

        cost = 2000
        player_balance = self.transactions.get_balance(ctx.author.id)
        if(player_balance < cost):
            return await self.utils.notify(ctx, "Can't Join", f"You need at least {cost:,} Eurodollar's to join the heist", "Heist")

        self.players.append(ctx.author.id)
        await self.transactions.withdraw(ctx.author.id, cost, "heist contribution", "anonymous")

        self.chance += 10
        await ctx.respond(f"{ctx.author.mention} has joined (Chance of success **{self.chance}%**)")

def setup(bot):
    bot.add_cog(Heist(bot))
