from discord.ext import commands
from database import getFact, addFact, saveRoles, getRoles
from russian_roulette import reload_function, pew_function

bot = commands.Bot(command_prefix='--', help_command=None)
token = str(input('Input token: '))


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_member_join(member):
    getRoles(member.id)

@bot.command(name='ping')
async def hello_command(ctx):
    await ctx.channel.send('pong')
    await ctx.channel.send(getRoles(ctx.message.author.id))


@bot.command(name='stop')
async def stop_command(ctx):
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
    if pew_function():
        saveRoles(ctx)
        await ctx.channel.send('**PEW**')
        await ctx.guild.get_member(ctx.message.author.id).kick()
    else:
        await ctx.channel.send('*click*')


@bot.command(name='suicide')
async def suicide_command(ctx):
    saveRoles(ctx)
    await ctx.channel.send('<@{0}> decidió que seguir viviendo no valía la pena'.format(ctx.message.author.id))
    await ctx.guild.get_member(ctx.message.author.id).kick()

bot.run(token)
