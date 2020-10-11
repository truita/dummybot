from os import getenv #Needed to get the arguments
from discord.ext import commands, tasks #The library for a discord bot (along with tasks to schedule loops)
#Imports functions from the other files on this project

import russian_roulette
from datetime import datetime, timedelta #Needed for scheduling
import music
import flags

bot = commands.Bot(command_prefix='.', help_command=None) #Creates the bot object
token = str(getenv('DISCORD_API_KEY'))


@bot.event
async def on_ready(): #Tells you when its ready
    print('We have logged in as {0.user}'.format(bot))
    flags.setup(bot)
    music.setup(bot)
    russian_roulette.setup(bot)

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
    future = datetime(2020, 6, 9, 00, 00)
    await ctx.channel.send('Quedan {0} hasta que salga satisfactory (approx)'.format(future - now))

@bot.command(name='google')
async def google_command(ctx, *, arg1):
    await ctx.channel.send("https://lmgtfy.com/?q={0}".format(arg1.replace(" ", "+")), embed=None)

bot.run(token)