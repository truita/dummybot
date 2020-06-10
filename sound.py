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
    await channel.connect()
async def leave_channel(ctx:commands.Context):
    guild = ctx.guild
    voice_client = guild.voice_client
    await voice_client.disconnect()

async def play(ctx,url):
    guild = ctx.guild
    voice_client = guild.voice_client
    await voice_client.create_yt_dl_player(url)