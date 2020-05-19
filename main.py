from discord.ext import commands
from database import getFact,addFact

bot = commands.Bot(command_prefix='--',help_command=None)
token = str(input('Input token: '))

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
@bot.command(name='ping')
async def hello_command(ctx):
    await ctx.channel.send('pong')
@bot.command(name='stop')
async def stop_command(ctx):
    await bot.close()
@bot.command(name='dato', aliases = ['fact'])
async def dato_command(ctx):
    await ctx.channel.send(getFact())
@bot.command(name='datoadd', aliases = ['adddato', 'addfact', 'añadirdato'])
async def datoadd_command(ctx,*,arg1):
    try:    
        addFact(arg1)
        await ctx.channel.send('Dato añadido!')
    except:
        await ctx.channel.send('Ha ocurrido un error al añadir tu dato')


bot.run(token)