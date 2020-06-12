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


async def pass_track(ctx,*,task=None):
    voice_client = ctx.guild.voice_client
    loop = voice_client.loop
    global track
    if task != None:
        while not task.done():
            asyncio.sleep(0.5)
    
    while not queue[track]:
        asyncio.sleep(0.5)
    try:
        current_song = queue[track]
    except:
        current_song = queue[len(queue) - 1]
    if not voice_client.is_playing() or not ctx.guild.voice_client.is_paused():
        loop.run_until_complete(voice_client.play(discord.FFmpegOpusAudio(current_song)))
        loop.call_soon_threadsafe(pass_track,ctx)
    else:
        ctx.guild.voice_client.source = discord.FFmpegOpusAudio(current_song)
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
    try:
        current_song = queue[track]
    except:
        current_song = queue[len(queue) - 1]
    guild = ctx.guild
    if guild.voice_client == None:
        await join_channel(ctx)
    voice_client = guild.voice_client
    if not voice_client.is_playing() or not voice_client.is_paused():
        task = asyncio.create_task(voice_client.play(discord.FFmpegOpusAudio(current_song)))
        asyncio.run(pass_track(ctx,task=task))
        
async def queue_read(ctx):
    await ctx.channel.send(queue)