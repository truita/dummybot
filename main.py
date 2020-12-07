from os import getenv  # Needed to get the arguments
# The library for a discord bot (along with tasks to schedule loops)
from discord.ext import commands
# Imports functions from the other files on this project

import misc
from datetime import datetime, timedelta  # Needed for scheduling
import music
import flags

# Creates the bot object
bot = commands.Bot(command_prefix='.', help_command=None)
token = str(getenv('DISCORD_API_KEY'))


@bot.event
async def on_ready():  # Tells you when its ready
    print('We have logged in as {0.user}'.format(bot))
    flags.setup(bot)
    music.setup(bot)
    misc.setup(bot)


@bot.command(name='ping')
async def ping_command(ctx: commands.Context):
    await ctx.channel.send('pong')


@bot.command(name='version')
async def version_command(ctx):
    # Sends current bot version over discord
    await ctx.channel.send('dummybot(py) v1.93 NO STABLE')


@bot.command(name='stop')
async def stop_command(ctx):
    if(ctx.message.author == ctx.guild.owner):
        await bot.close()

# Calculates the time between now and 00:00
@bot.command(name='poletime', aliases=['timepole', 'nextpole', 'timeleft'])
async def poletime_command(ctx: commands.Context):
    now = datetime.now()
    future = datetime(now.year, now.month, now.day, 00, 00)
    if now.hour >= 00 and now.minute > 00:
        future += timedelta(days=1)
    await ctx.channel.send('Queda {0} hasta la siguiente pole'.format(future - now))


@bot.command(name='satisfactory')
async def satisfactory_command(ctx: commands.Context):
    now = datetime.now()
    future = datetime(2020, 6, 9, 00, 00)
    await ctx.channel.send('Quedan {0} hasta que salga satisfactory (approx)'.format(future - now))


@bot.command(name='google')
async def google_command(ctx, *, arg1):
    await ctx.channel.send("https://lmgtfy.com/?q={0}".format(arg1.replace(" ", "+")), embed=None)

bot.run(token)
