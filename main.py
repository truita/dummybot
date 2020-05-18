from discord.ext import commands
from database import getFact
import sys

bot = commands.Bot(command_prefix='--',help_command=None)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
@bot.command(name='ping')
async def hello_command(ctx):
    await ctx.channel.send('pong')
@bot.command(name='stop')
async def stop_command(ctx):
    await bot.close()
@bot.command(name='dato')
async def dato_command(ctx):
    await ctx.channel.send(getFact())


bot.run('NzAyMDk3MzgxMTg5MDkxNDE5.XsK3GA.IdC8JTZ3N5AbqJrAmVM8u70x2BE')