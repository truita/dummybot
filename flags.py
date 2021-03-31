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
    flag_number_to_string = ["pole", "subpole", "fail"]

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
        flags = [True, True, True]
        makers = [0, 0, 0]

    # Returns a tuple [Whether the flag is taken, [If you have already taken a flag, The flag you've taken]]
    def get_flag_info(self, flagtype, guild, maker):
        if guild in self.readyflags:
            guild_flags = self.readyflags[guild]
            if guild_flags.flags[flagtype] != True:
                return (False, guild_flags.makers[flagtype])
            elif maker in (guild_flags.makers[:flagtype] + guild_flags.makers[flagtype:]):
                return (False, (True, guild_flags.index(maker)))
            else:
                return (True, None)

        else:
            self.readyflags[guild] = self.FlagChecks()
            self.readyflags[guild].flags[flagtype] = False
            return (True, None)

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
        flag_info = self.get_flag_info(0, ctx.guild.id, ctx.author.id)
        guild_flags = self.readyflags[ctx.guild.id]
        if flag_info[0] == True:
            conn = database_utils.get_conn(ctx.guild.id)
            conn.execute(
                "INSERT INTO FLAGS(ID,POINTS,POLE) VALUES(?,4,1) ON CONFLICT(ID) DO UPDATE SET POINTS = POINTS + 4, POLE = POLE + 1", (ctx.author.id,))
            guild_flags.flags[0] = False
            guild_flags.makers[0] = ctx.author.id
            await ctx.send(f'{ctx.author.mention} ha hecho la pole!')
        elif flag_info[1][0] == True:
            await ctx.send(f'{ctx.author.mention} ya has hecho .{self.flag_number_to_string[flag_info[1][1]]}')
        elif flag_info[0] == False:
            await ctx.send(f'<@{guild_flags.makers[0]}> ya ha hecho la pole')

    @commands.command()
    async def subpole(self, ctx):
        flag_info = self.get_flag_info(1, ctx.guild.id, ctx.author.id)
        guild_flags = self.readyflags[ctx.guild.id]
        if flag_info[0] == True:
            conn = database_utils.get_conn(ctx.guild.id)
            conn.execute(
                "INSERT INTO FLAGS(ID,POINTS,SUBPOLE) VALUES(?,2,1) ON CONFLICT(ID) DO UPDATE SET POINTS = POINTS + 2, SUBPOLE = SUBPOLE + 1", (ctx.author.id,))
            guild_flags.flags[1] = False
            guild_flags.makers[1] = ctx.author.id
            await ctx.send(f'{ctx.author.mention} ha hecho la pole!')
        elif flag_info[1][0] == True:
            await ctx.send(f'{ctx.author.mention} ya has hecho .{self.flag_number_to_string[flag_info[1][1]]}')
        elif flag_info[0] == False:
            await ctx.send(f'<@{guild_flags.makers[1]}> ya ha hecho la pole')

    @commands.command()
    async def fail(self, ctx):
        flag_info = self.get_flag_info(2, ctx.guild.id, ctx.author.id)
        guild_flags = self.readyflags[ctx.guild.id]
        if flag_info[0] == True:
            conn = database_utils.get_conn(ctx.guild.id)
            conn.execute(
                "INSERT INTO FLAGS(ID,POINTS,FAIL) VALUES(?,1,1) ON CONFLICT(ID) DO UPDATE SET POINTS = POINTS + 1, FAIL = FAIL + 1", (ctx.author.id,))
            guild_flags.flags[2] = False
            guild_flags.makers[2] = ctx.author.id
            await ctx.send(f'{ctx.author.mention} ha hecho la pole!')
        elif flag_info[1][0] == True:
            await ctx.send(f'{ctx.author.mention} ya has hecho .{self.flag_number_to_string[flag_info[1][1]]}')
        elif flag_info[0] == False:
            await ctx.send(f'<@{guild_flags.makers[2]}> ya ha hecho la pole')

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
