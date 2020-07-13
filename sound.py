import youtube_dl
from discord.ext import commands
import discord
import os, asyncio

class MusicManager():
    DOWNLOAD_PATH = "/tmp/dummybot"
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
            self.guild_tracks[guild.id] = -1
    
    async def leave_channel(self,ctx:commands.Context):
        guild = ctx.guild
        voice_client = guild.voice_client
        await voice_client.disconnect()
        self.guild_queues[guild.id] = []
        self.guild_tracks[guild.id] = -1

    def queue(self,guild:discord.guild, song_id):
        song_file = "{0}/{1}".format(self.DOWNLOAD_PATH, song_id)
        self.guild_queues[guild.id].append(song_file)
        self.guild_tracks[guild.id] += 1
    
    def play(self,ctx:commands.Context, arg):
        voice_client = ctx.guild.voice_client
        with youtube_dl.YoutubeDL({'format': 'bestaudio/opus', 'outtmpl': '{0}/%(id)s'.format(self.DOWNLOAD_PATH)}) as ydl:
            song_info = ydl.extract_info(arg, False)
            ydl.download([arg])
        self.queue(ctx.guild, song_info["id"])
        if not voice_client.is_playing():
            loop = asyncio.get_event_loop()
            current_song = self.guild_queues[ctx.guild.id][self.guild_tracks[ctx.guild.id]]
            voice_client.play(discord.FFmpegOpusAudio(current_song, codec="copy"), after=lambda a: loop.create_task(self.next_song(ctx)))

    async def next_song(self, ctx):
        if self.guild_queues[ctx.guild.id] == None:
            return
        loop = asyncio.get_event_loop()
        current_song = self.guild_queues[ctx.guild.id][self.guild_tracks[ctx.guild.id]]
        voice_client = ctx.guild.voice_client
        voice_client.play(discord.FFmpegOpusAudio(current_song, codec="copy"), after=lambda a: loop.create_task(self.next_song(ctx)))