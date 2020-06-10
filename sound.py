import youtube_dl
from discord.ext import commands
import discord
import os

queue = []
track = 0

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

async def pass_track(ctx):
    global track
    global player
    voice_client = ctx.guild.voice_client
    player.stop()
    player = await voice_client.play(discord.FFmpegOpusAudio(queue[track]))

async def play(ctx,url):
    filename = ""
    global track
    guild = ctx.guild
    voice_client = guild.voice_client
    with youtube_dl.YoutubeDL({'format': 'bestaudio/best', 'outtmpl': '/tmp/dummybot/{0}.webm'.format(track)}) as ydl:
        ydl.download([url])
        filename = "/tmp/dummybot/{0}.webm".format(track)
        global queue
        queue.append(filename)

    
    if not voice_client.is_playing() or not voice_client.is_paused():
        global player
        player = await voice_client.play(discord.FFmpegOpusAudio(queue[track]))
        track += 1
        