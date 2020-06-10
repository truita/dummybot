import youtube_dl
from discord.ext import commands
import discord
import os

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
    youtube_dl.YoutubeDL({'format': 'bestaudio/best'}).download(url)
    for file in os.listdir("./"):
        if(file.endswith([".weba",".mp3",".webm",])):
            os.rename("song.mp3")
    player = await voice_client.play(discord.FFmpegOpusAudio("song.mp3"))
    users[guild.id] = player