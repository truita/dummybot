import youtube_dl
from discord.ext import commands
import discord
import os

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

async def pass_track(ctx):
    global track
    global player
    player.source = discord.FFmpegOpusAudio(queue[track])

def download(url):
    filename = ""
    global track
    youtube_dl.YoutubeDL({'format': 'bestaudio/best', 'outtmpl': '/tmp/dummybot/{0}.webm'.format(track)}).download([url])
    filename = "/tmp/dummybot/{0}.webm".format(track)
    global queue
    queue.append(filename)
    
async def play(ctx,url):
    global track
    track += 1
    download(url)
    guild = ctx.guild
    voice_client = guild.voice_client
    if not voice_client.is_playing() or not voice_client.is_paused():
        global player
        player = await voice_client.play(discord.FFmpegOpusAudio(queue[track]))
        
        