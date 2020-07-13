import youtube_dl
from discord.ext import commands
import discord
import os, asyncio

class MusicManager():
    DOWNLOAD_PATH = "/tmp/dummybot"
    guild_queues = {}
    guild_tracks = {}
    guild_loop = {}

    async def join_channel(self,ctx:commands.Context):
        if ctx.author.voice == None:
            await ctx.channel.send("No estás conectado a un canal de voz!")
        else:
            channel = ctx.author.voice.channel
            guild = ctx.guild
            await channel.connect()
            self.guild_queues[guild.id] = []
            self.guild_tracks[guild.id] = 0
            self.guild_loop[guild.id] = False
    
    async def leave_channel(self,ctx:commands.Context):
        guild = ctx.guild
        voice_client = guild.voice_client
        await voice_client.disconnect()
        self.guild_queues[guild.id] = []
        self.guild_tracks[guild.id] = 0
        self.guild_loop[guild.id] = False

    def __queue__(self,guild:discord.guild, song_id):
        for i in song_id:
            song_file = "{0}/{1}".format(self.DOWNLOAD_PATH, i)
            self.guild_queues[guild.id].append(song_file)
    
    async def download(self,url, after):
        with youtube_dl.YoutubeDL({'format': 'bestaudio/opus','default_search': 'ytsearch1','outtmpl': '{0}/%(id)s'.format(self.DOWNLOAD_PATH), 'nooverwrites': True}) as ydl:
            ydl.download([url])
        after()
    
    def __do_play__(self,ctx):
        if ctx.guild.voice_client == None:
            asyncio.run(self.join_channel(ctx))
        voice_client = ctx.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()
        loop = asyncio.get_event_loop()
        current_song = self.guild_queues[ctx.guild.id][self.guild_tracks[ctx.guild.id]]
        voice_client.play(discord.FFmpegOpusAudio(current_song, codec="copy"), after=lambda a: loop.create_task(self.next_song(ctx)))
    
    async def play(self,ctx:commands.Context, arg):
        loop = asyncio.get_event_loop()

        with youtube_dl.YoutubeDL({'format': 'bestaudio/opus', 'default_search': 'ytsearch1'}) as ydl:
            song_info = ydl.extract_info(arg, False)

        song_id = []
        if "entries" in song_info.keys():
            for i in song_info["entries"]:
                song_id.append(i["id"])
        else:
            song_id.append(song_info["id"])

        self.__queue__(ctx.guild, song_id)
        if not ctx.guild.voice_client.is_playing():
            loop.create_task(self.download(arg, lambda: self.__do_play__(ctx)))

    async def next_song(self, ctx):
        self.guild_tracks[ctx.guild.id] += 1

        if self.guild_queues[ctx.guild.id] == None:
            return
        
        if len(self.guild_queues[ctx.guild.id]) - 1 < self.guild_tracks[ctx.guild.id]:
            if self.guild_loop[ctx.guild.id] == True:
                self.guild_tracks[ctx.guild.id] = 0
            else:
                await self.leave_channel(ctx)
                return
        
        self.__do_play__(ctx)