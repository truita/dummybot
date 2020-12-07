import discord
import sqlite3
import os
import database_utils
import asyncio
from datetime import datetime, timedelta
from discord.ext import commands, tasks
from operator import itemgetter


class Flags(commands.Cog):
    readyflags = {}

    def __init__(self, bot):
        self.bot = bot
        sql = """CREATE TABLE IF NOT EXISTS FLAGS (
                    ID INTEGER NOT NULL PRIMARY KEY, 
                    POINTS INTEGER DEFAULT 0 NOT NULL,
                    POLE INTEGER DEFAULT 0 NOT NULL,
                    SUBPOLE INTEGER DEFAULT 0 NOT NULL,
                    FAIL INTEGER DEFAULT 0 NOT NULL);"""
        database_utils.execute_on_all_db(sql)
        self.reset_flags.start()

    class FlagChecks():
        pole = True
        subpole = True
        fail = True

        pole_maker = 0
        subpole_maker = 0
        fail_maker = 0

        def cases(self, flagtype):
            if flagtype == "pole":
                return (("subpole", self.subpole, self.subpole_maker), ("fail", self.fail, self.fail_maker))
            if flagtype == "subpole":
                return (("pole", self.pole, self.pole_maker), ("fail", self.fail, self.fail_maker))
            if flagtype == "fail":
                return (("pole", self.pole, self.pole_maker), ("subpole", self.subpole, self.subpole_maker))

    # 0 = Flag is unavalaible, 1 = Flag is avalaible, *FlagType* = A user has already taken *FlagType*
    def is_flag_ready(self, flagtype, guild, maker):
        if guild in self.readyflags:
            if not getattr(self.readyflags[guild], flagtype):
                return 0
            for pack in self.readyflags[guild].cases(flagtype):
                if pack[2] == maker:
                    return pack[0]
            return 1

        else:
            self.readyflags[guild] = self.FlagChecks()
            setattr(self.readyflags[guild], f"{flagtype}", False)
            return 0

    @tasks.loop(hours=24)
    async def reset_flags(self):
        for guild in self.readyflags:

            guild.pole = True
            guild.subpole = True
            guild.fail = True

            guild.pole_maker = 0
            guild.subpole_maker = 0
            guild.fail_maker = 0

    @reset_flags.before_loop
    async def before_reset_flags(self):
        hour = 00
        minute = 00
        now = datetime.now()
        target = datetime(now.year, now.month, now.day, hour, minute)
        if now.hour >= hour and now.minute > minute:
            target += timedelta(days=1)
        await asyncio.sleep((target - now).total_seconds())

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        conn = database_utils.get_conn(guild.id)
        sql = """CREATE TABLE FLAGS (
                    ID INTEGER NOT NULL PRIMARY KEY, 
                    POINTS INTEGER DEFAULT 0 NOT NULL,
                    POLE INTEGER DEFAULT 0 NOT NULL,
                    SUBPOLE INTEGER DEFAULT 0 NOT NULL,
                    FAIL INTEGER DEFAULT 0 NOT NULL);"""

        conn.execute(sql)
        conn.close()

    async def cog_before_invoke(self, ctx):
        guild_check = ctx.guild is not None
        return guild_check

    @commands.command()
    async def pole(self, ctx):
        flagstatus = self.is_flag_ready("pole", ctx.guild.id, ctx.author.id)
        if flagstatus == 1:
            conn = database_utils.get_conn(ctx.guild.id)
            conn.execute(
                "INSERT INTO FLAGS(ID,POINTS,POLE) VALUES(?,4,1) ON CONFLICT(ID) DO UPDATE SET POINTS = POINTS + 4, POLE = POLE + 1", (ctx.author.id,))
            self.readyflags[ctx.guild.id].pole = False
            self.readyflags[ctx.guild.id].pole_maker = ctx.author.id
            await ctx.send(f'{ctx.author.mention} ha hecho la pole!')
        elif flagstatus == 0:
            await ctx.send(f'<@{self.readyflags[ctx.guild.id].pole_maker}> ya ha hecho la pole')
        elif isinstance(flagstatus, str):
            await ctx.send(f'{ctx.author.mention} ya has hecho .{flagstatus}')

    @commands.command()
    async def subpole(self, ctx):
        flagstatus = self.is_flag_ready("subpole", ctx.guild.id, ctx.author.id)
        if flagstatus == 1:
            conn = database_utils.get_conn(ctx.guild.id)
            conn.execute(
                "INSERT INTO FLAGS(ID,POINTS,SUBPOLE) VALUES(?,2,1) ON CONFLICT(ID) DO UPDATE SET POINTS = POINTS + 2, SUBPOLE = SUBPOLE + 1", (ctx.author.id,))
            self.readyflags[ctx.guild.id].subpole = False
            self.readyflags[ctx.guild.id].subpole_maker = ctx.author.id
            await ctx.send(f'{ctx.author.mention} ha hecho la subpole!')
        elif flagstatus == 0:
            await ctx.send(f'<@{self.readyflags[ctx.guild.id].subpole_maker}> ya ha hecho la subpole')
        elif isinstance(flagstatus, str):
            await ctx.send(f'{ctx.author.mention} ya has hecho .{flagstatus}')

    @commands.command()
    async def fail(self, ctx):
        flagstatus = self.is_flag_ready("fail", ctx.guild.id, ctx.author.id)
        if flagstatus == 1:
            conn = database_utils.get_conn(ctx.guild.id)
            conn.execute(
                "INSERT INTO FLAGS(ID,POINTS,FAIL) VALUES(?,1,1) ON CONFLICT(ID) DO UPDATE SET POINTS = POINTS + 1, FAIL = FAIL + 1", (ctx.author.id,))
            self.readyflags[ctx.guild.id].fail = False
            self.readyflags[ctx.guild.id].fail_maker = ctx.author.id
            await ctx.send(f'{ctx.author.mention} ha hecho el fail!')
        elif flagstatus == 0:
            await ctx.send(f'<@{self.readyflags[ctx.guild.id].fail_maker}> ya ha hecho el fail')
        elif isinstance(flagstatus, str):
            await ctx.send(f'{ctx.author.mention} ya has hecho .{flagstatus}')

    @commands.command()
    async def ranking(self, ctx):
        conn = database_utils.get_conn(ctx.guild.id)
        points = conn.execute("SELECT * FROM FLAGS").fetchall()
        description = ""

        total_points = sorted(points, key=itemgetter(1), reverse=True)
        pole_points = sorted(points, key=itemgetter(2), reverse=True)
        subpole_points = sorted(points, key=itemgetter(3), reverse=True)
        fail_points = sorted(points, key=itemgetter(4), reverse=True)

        emoticon_list = (":one:", ":two:", ":three:", ":vs:", ":vs:")

        description += """:checkered_flag: :earth_africa: **RANKING GLOBAL** :earth_africa: :checkered_flag:\n----------------------------------------\n"""
        for idx, member in enumerate(total_points):
            if idx >= 5:
                break
            description += f"{emoticon_list[idx]}<@{member[0]}> => {member[1]}\n"
        description += """:checkered_flag: :one: **POLE** :one: :checkered_flag:\n----------------------------------------\n"""
        for idx, member in enumerate(pole_points):
            if idx >= 5:
                break
            description += f"{emoticon_list[idx]}<@{member[0]}> => {member[2]}\n"
        description += """:checkered_flag: :two: **SUBPOLE** :two: :checkered_flag:\n----------------------------------------\n"""
        for idx, member in enumerate(subpole_points):
            if idx >= 5:
                break
            description += f"{emoticon_list[idx]}<@{member[0]}> => {member[3]}\n"
        description += """:checkered_flag: :three: **FAIL** :three: :checkered_flag:\n----------------------------------------\n"""
        for idx, member in enumerate(fail_points):
            if idx >= 5:
                break
            description += f"{emoticon_list[idx]}<@{member[0]}> => {member[4]}\n"

        embed = discord.Embed(colour=discord.Colour.blue(),
                              description=description)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Flags(bot))
