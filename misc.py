import random
import os
import discord
from discord.ext import commands
import database_utils


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
            self.magazine[random.randint(0, 5)] = 1
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
        magazine_exists = ctx.guild.id in self.guns is False
        magazine_not_reloaded = self.guns[ctx.guild.id].reloaded is False
        if magazine_exists or magazine_not_reloaded:
            await ctx.send("Recarga antes de disparar!")
        else:
            if self.guns[ctx.guild.id].shoot():
                await ctx.channel.send('**PEW**')
                invite = await ctx.channel.create_invite(max_uses=1)
                await ctx.message.author.send(invite)
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

class Facts(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        sql = """CREATE TABLE IF NOT EXISTS "FACTS" (
                "FACT"  TEXT NOT NULL,
                PRIMARY KEY("FACT")
               );"""
        database_utils.execute_on_all_db(sql)

    async def cog_before_invoke(self, ctx):
        guild_check = ctx.guild is not None
        return guild_check

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        conn = database_utils.get_conn(guild.id)
        sql = """CREATE TABLE "FACTS"("FACT" TEXT NOT NULL,PRIMARY KEY("FACT"));"""
        conn.execute(sql)
        conn.close()

    @commands.command(aliases=['dato'])
    async def fact(self, ctx):
        conn = database_utils.get_conn(ctx.guild.id)
        facts = conn.execute('SELECT "FACT" FROM FACTS').fetchall()
        selected_fact = facts[random.randint(0, len(facts) - 1)][0]
        await ctx.send(selected_fact)

    @commands.command(aliases=['datoadd', 'añadirdato'])
    async def addfact(self, ctx, *, dato):
        conn = database_utils.get_conn(ctx.guild.id)
        try:
            conn.execute('INSERT INTO FACTS(FACT) VALUES (?)', (dato,))
        except database_utils.sqlite3.Error as error:
            await ctx.send("Ha ocurrido un error! {0}".format(error))
            return
        await ctx.send("Dato añadido!")


def setup(bot):
    bot.add_cog(RussianRoulette(bot))
    bot.add_cog(Facts(bot))
