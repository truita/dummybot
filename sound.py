import youtube_dl
from discord.ext import commands
import discord
import os, asyncio

queue = []
track = -1


class MusicManager():
    guild_queues = {}
    guild_tracks = {}

    async def join_channel(self,ctx:commands.Context):
        if ctx.author.voice == None:
            await ctx.channel.send("No estás conectado a un canal de voz!")
        else:
            channel = ctx.author.voice.channel
            guild = ctx.guild
            await channel.connect()
            self.guild_queues[guild.id] = []
            self.guild_tracks[guild.id] = 0
    
    async def leave_channel(self,ctx:commands.Context):
        guild = ctx.guild
        voice_client = guild.voice_client
        await voice_client.disconnect()
        global queue, track
        self.guild_queues[guild.id] = []
        self.guild_tracks[guild.id] = 0    