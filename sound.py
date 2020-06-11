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
    track = track
    if not ctx.guild.voice_client.is_playing() or not ctx.guild.voice_client.is_paused():
        await ctx.guild.voice_client.play(discord.FFmpegOpusAudio(queue[track]))
    else:
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
    try:
        download(url, track)
    except:
        ctx.channel.send('Error encontrando tu canción')
        track -= 1
    guild = ctx.guild
    if guild.voice_client == None:
        await join_channel(ctx)
    voice_client = guild.voice_client
    if not voice_client.is_playing() or not voice_client.is_paused():
        voice_client.play(discord.FFmpegOpusAudio(queue[track]))
        print('Music Finished!')
        await pass_track(ctx)
        
async def queue_read(ctx):
    await ctx.channel.send(queue)