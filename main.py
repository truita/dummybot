import sys
from discord.ext import commands, tasks
from database import getFact, addFact, saveRoles, restoreRoles
from russian_roulette import reload_function, pew_function
from pole import pole, subpole, fail, resetpole, ranking
from datetime import datetime, timedelta
import asyncio

bot = commands.Bot(command_prefix='.', help_command=None)
token = str(sys.argv[1])

@tasks.loop(hours=24)
async def pole_schedule():
    resetpole()

@pole_schedule.before_loop
async def before_pole_schedule():
    hour = 00 
    minute = 00
    await bot.wait_until_ready()
    now = datetime.now()
    future = datetime(now.year, now.month, now.day, hour, minute)
    if now.hour >= hour and now.minute > minute:
        future += timedelta(days=1)
    await asyncio.sleep((future - now).total_seconds())

pole_schedule.start()

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_member_join(member):
    await restoreRoles(member)

@bot.command(name='ping')
async def ping_command(ctx:commands.Context):
    await ctx.channel.send('pong')

@bot.command(name='version')
async def version_command(ctx):
    await ctx.channel.send('dummybot(py) v1.00')

@bot.command(name='stop')
async def stop_command(ctx):
    if(ctx.message.author == ctx.guild.owner):
        await bot.close()


@bot.command(name='dato', aliases=['fact'])
async def dato_command(ctx):
    await ctx.channel.send(getFact())


@bot.command(name='datoadd', aliases=['adddato', 'addfact', 'añadirdato'])
async def datoadd_command(ctx, *, arg1):
    try:
        addFact(arg1)
        await ctx.channel.send('Dato añadido!')
    except:
        await ctx.channel.send('Ha ocurrido un error al añadir tu dato')


@bot.command(name='reload')
async def reload_command(ctx):
    reload_function()
    await ctx.channel.send('clac clac')


@bot.command(name='pew')
async def pew_command(ctx):
    pew_result = pew_function()
    if pew_result == 2:
        await ctx.channel.send('Recarga antes de disparar!')
    elif pew_result == 1:
        saveRoles(ctx)
        await ctx.channel.send('**PEW**')
        await ctx.message.author.send(await ctx.channel.create_invite(max_uses=1))
        try:
            await ctx.message.author.kick()
        except:
            await ctx.channel.send('No tengo permisos suficientes!')
    else:
        await ctx.channel.send('*click*')


@bot.command(name='suicide')
async def suicide_command(ctx):
    saveRoles(ctx)
    await ctx.channel.send('<@{0}> decidió que seguir viviendo no valía la pena'.format(ctx.message.author.id))
    await ctx.message.author.send(await ctx.channel.create_invite(max_uses=1))
    try:
        await ctx.message.author.kick()
    except:
        await ctx.channel.send('No tengo permisos suficientes!')

@bot.command(name='poletime', aliases=['timepole','nextpole','timeleft'])
async def poletime_command(ctx:commands.Context):
    now = datetime.now()
    future = datetime(now.year, now.month, now.day, 00, 00)
    if now.hour >= 00 and now.minute > 00:
        future += timedelta(days=1)
    await ctx.channel.send('Queda {0} hasta la siguiente pole'.format(future))

@bot.command(name='pole', aliases=['Pole'])
async def pole_command(ctx):
    await pole(ctx)

@bot.command(name='subpole', aliases=['Subpole'])
async def subpole_command(ctx):
    await subpole(ctx)

@bot.command(name='fail', aliases=['Fail'])
async def fail_command(ctx):
    await fail(ctx)

@bot.command(name='ranking')
async def ranking_command(ctx):
    await ranking(ctx)
bot.run(token)
