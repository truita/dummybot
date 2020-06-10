import youtube_dl
from discord.ext import commands

users = {}

def initialize_voice(bot_argument:commands.Bot):
    global bot
    bot = bot_argument

async def join_channel(ctx:commands.Context):
    try:
        channel = ctx.author.voice.channel
    except:
        await ctx.channel.send("No estás en un canal de voz!")
    await bot.join_voice_channel(channel)

async def leave_channel(ctx:commands.Context):
    guild = ctx.guild
    voice_client = bot.voice_client_in(guild)
    await voice_client.disconnect()