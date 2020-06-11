import youtube_dl
from discord.ext import commands
import discord
import os, asyncio

queue = []
track = -1

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
    global queue, track
    queue = []
    track = -1

async def pass_track(ctx):
    global track
    while not queue[track]:
        asyncio.run(asyncio.sleep(0.5))
    ctx.guild.voice_client.source = discord.FFmpegOpusAudio(queue[track])
    track += 1

def download(url, track):
    with youtube_dl.YoutubeDL({'format': 'bestaudio/best', 'outtmpl': '/tmp/dummybot/%(id)s.webm'}) as ydl:
        ydl.download([url])
        filename = "/tmp/dummybot/{0}.webm".format(ydl.extract_info(url)['id'])
    global queue
    queue.append(filename)
    
async def play(ctx,url):
    global track
    track += 1
    download(url, track)
    guild = ctx.guild
    voice_client = guild.voice_client
    if not voice_client.is_playing() or not voice_client.is_paused():
        await voice_client.play(discord.FFmpegOpusAudio(queue[track]))
        pass_track(ctx)
        
        