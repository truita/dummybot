import sys #Needed to get the arguments
from discord.ext import commands, tasks #The library for a discord bot (along with tasks to schedule loops)
#Imports functions from the other files on this project
from database import getFact, addFact, saveRoles, restoreRoles
from russian_roulette import reload_function, pew_function
from pole import pole, subpole, fail, resetpole, ranking
from sound import MusicManager
#
from datetime import datetime, timedelta #Needed for scheduling
import asyncio #Also needed for scheduling

bot = commands.Bot(command_prefix='.', help_command=None) #Creates the bot object
token = str(sys.argv[1]) #Gets the bot token from the arguments
music = MusicManager()

@tasks.loop(hours=24) #Every 24 hours resets pole variables
async def pole_schedule():
    resetpole()

@pole_schedule.before_loop #Calculates time until 00:00 and waits that time for the pole_schedule loop to run exactly at 00:00 every day
async def before_pole_schedule():
    hour = 00 
    minute = 00
    await bot.wait_until_ready()
    now = datetime.now()
    future = datetime(now.year, now.month, now.day, hour, minute)
    if now.hour >= hour and now.minute > minute:
        future += timedelta(days=1)
    await asyncio.sleep((future - now).total_seconds())

pole_schedule.start() #Starts the loop

@bot.event
async def on_ready(): #Tells you when its ready
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_member_join(member): #Restores (or tries to) restore the roles of the person who joins
    try:
        await restoreRoles(member)
    except:
        pass

@bot.command(name='ping')
async def ping_command(ctx:commands.Context):
    await ctx.channel.send('pong')

@bot.command(name='version')
async def version_command(ctx):
    await ctx.channel.send('dummybot(py) v1.92 NO STABLE') #Sends current bot version over discord

@bot.command(name='stop')
async def stop_command(ctx):
    if(ctx.message.author == ctx.guild.owner): #Only if the owner asks to, the bot stops
        await bot.close()


@bot.command(name='dato', aliases=['fact'])
async def dato_command(ctx):
    await ctx.channel.send(getFact()) #Gets a fact from the database and sends it


@bot.command(name='datoadd', aliases=['adddato', 'addfact', 'añadirdato'])
async def datoadd_command(ctx, *, arg1):
    try: #Tries to add the fact to the database
        addFact(arg1)
        await ctx.channel.send('Dato añadido!')
    except:
        await ctx.channel.send('Ha ocurrido un error al añadir tu dato') #If something goes wrong it will throw an error


@bot.command(name='reload')
async def reload_command(ctx): #Reloads the magazine
    reload_function()
    await ctx.channel.send('clac clac')


@bot.command(name='pew')
async def pew_command(ctx):
    pew_result = pew_function()
    if pew_result == 2: # 2 = no bullets
        await ctx.channel.send('Recarga antes de disparar!')
    elif pew_result == 1: # 1 = bullet hit
        saveRoles(ctx)
        await ctx.channel.send('**PEW**')
        await ctx.message.author.send(await ctx.channel.create_invite(max_uses=1))
        try:
            await ctx.message.author.kick()
        except:
            await ctx.channel.send('No tengo permisos suficientes!')
    else: # 0 = bullets in magazine, but didn't hit
        await ctx.channel.send('*click*')


@bot.command(name='suicide')
async def suicide_command(ctx):
    saveRoles(ctx) #Saves its roles before kicking
    await ctx.channel.send('<@{0}> decidió que seguir viviendo no valía la pena'.format(ctx.message.author.id))
    await ctx.message.author.send(await ctx.channel.create_invite(max_uses=1)) #Sends him/her an invite back to the server
    try:
        await ctx.message.author.kick() #Kicks
    except:
        await ctx.channel.send('No tengo permisos suficientes!') #If it has no perms it will show this

@bot.command(name='poletime', aliases=['timepole','nextpole','timeleft']) #This whole function just calculates the time between now and 00:00
async def poletime_command(ctx:commands.Context):
    now = datetime.now()
    future = datetime(now.year, now.month, now.day, 00, 00)
    if now.hour >= 00 and now.minute > 00:
        future += timedelta(days=1)
    await ctx.channel.send('Queda {0} hasta la siguiente pole'.format(future - now))

@bot.command(name='satisfactory')
async def satisfactory_command(ctx:commands.Context):
    now = datetime.now()
    future = datetime(now.year, now.month, 9, 00, 00)
    await ctx.channel.send('Quedan {0} hasta que salga satisfactory (approx)'.format(future - now))

#All the following functions are further explained in pole.py
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


@bot.command(name='google')
async def google_command(ctx, *, arg1):
    await ctx.channel.send("https://lmgtfy.com/?q={0}".format(arg1.replace(" ", "+")), embed=None)

@bot.command(name='join')
async def join_command(ctx):
    await music.join_channel(ctx)

@bot.command(name='leave')
async def leave_command(ctx):
    await music.leave_channel(ctx)

@bot.command(name='play')
async def play_command(ctx, *, args):
    await music.play(ctx, args)

@bot.command(name='next')
async def next_command(ctx):
    await music.next_song(ctx)

@bot.command(name='shuffle')
async def shuffle_command(ctx):
    await music.shuffle(ctx)

@bot.command(name='loop')
async def loop_command(ctx):
    await music.loop(ctx)

bot.run(token)