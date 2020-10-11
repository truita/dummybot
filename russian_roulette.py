import random
import discord
from discord.ext import commands


class RussianRoulette(commands.Cog):
    guns = {}

    def __init__(self, bot):
        self.bot = bot

    async def cog_before_invoke(self, ctx):
        guild_check = ctx.guild is not None
        return guild_check

    class Gun():
        magazine = [0] * 6
        position = 0
        reloaded = False

        def reload(self):
            self.magazine[random.randint(0,5)] = 1
            self.position = 0
            self.reloaded = True
        
        def shoot(self):
            if self.magazine[self.position] == 1:
                self.reloaded = False
                return 1
            else:
                self.position += 1
                return 0

    @commands.command()
    async def pew(self, ctx: commands.Context):
        if ctx.guild.id not in self.guns or self.guns[ctx.guild.id].reloaded == False:
            await ctx.send("Recarga antes de disparar!")
        else:
            if self.guns[ctx.guild.id].shoot():
                await ctx.channel.send('**PEW**')
                await ctx.message.author.send(await ctx.channel.create_invite(max_uses=1))
                try:
                    await ctx.author.kick()
                except discord.Forbidden:
                    await ctx.send('No tengo permisos suficientes!')
            else:
                await ctx.send("*clic*")

    @commands.command()
    async def reload(self, ctx):
        if ctx.guild.id not in self.guns:
            self.guns[ctx.guild.id] = self.Gun()
        self.guns[ctx.guild.id].reload()
        await ctx.send("*clac clac*")

        
def setup(bot):
    bot.add_cog(RussianRoulette(bot))