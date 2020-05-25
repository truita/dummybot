from database import savePole,saveSubpole,saveFail

pole_ready = False
subpole_ready = False
fail_ready = False

pole_maker = None
subpole_maker = None
fail_maker = None

def resetpole():
    global pole_maker,subpole_maker,fail_maker
    global pole_ready,subpole_ready,fail_ready
    
    pole_ready = False
    subpole_ready = False
    fail_ready = False

    pole_maker = None
    subpole_maker = None
    fail_maker = None


async def pole(ctx):
    global pole_ready
    global pole_maker
    if not pole_ready:
        await ctx.channel.send("La pole ya ha sido realizada por <@{0}>".format(pole_maker))
        return
    elif subpole_maker == ctx.message.author.id:
        await ctx.channel.send("<@{0}> ya has hecho la subpole!".format(subpole_maker))
        return
    elif fail_maker == ctx.message.author.id:
        await ctx.channel.send("<@{0}> ya has hecho el fail!".format(fail_maker))
        return
    else:
        savePole(ctx.message.author.id)
        await ctx.channel.send("<@{0}> ha hecho la pole!".format(ctx.message.author.id))
        return