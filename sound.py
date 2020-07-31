from pytube import YouTube
import pyyoutube
from discord.ext import commands
import discord
import os
import asyncio
import random

api = pyyoutube.Api(api_key=os.getenv("YOUTUBE_API_KEY"))

class MusicManager():
    guild_queues = {}
    guild_tracks = {}
    guild_loop = {}

    def __prepare__(self, ctx):
        guild = ctx.guild
        self.guild_queues[guild.id] = []
        self.guild_tracks[guild.id] = 0
        self.guild_loop[guild.id] = False

    async def join_channel(self,ctx:commands.Context):
        if ctx.author.voice is None:
            await ctx.channel.send("No estás conectado a un canal de voz!")
        else:
            channel = ctx.author.voice.channel
            await channel.connect()
            
    
    async def leave_channel(self,ctx:commands.Context):
        if ctx.author.voice.channel == ctx.guild.voice_client.channel:
            guild = ctx.guild
            voice_client = guild.voice_client
            await voice_client.disconnect()

    def __queue__(self,guild:discord.guild, song_id):
        for song_file in song_id:
            self.guild_queues[guild.id].append(song_file)
    
    
    async def __do_play__(self,ctx):
        video_id = self.guild_queues[ctx.guild.id][self.guild_tracks[ctx.guild.id]]
        video_url = "https://youtube.com/watch?v={0}".format(video_id)
        video_name = api.get_video_by_id(video_id=video_id).items[0].snippet.title
        msg_embed = discord.Embed(
            colour=discord.Colour.blue(),
            title="Now Playing",
            description="[{0}]({1})[{2}]".format(video_name, video_url, ctx.author.mention)
        )
        await ctx.channel.send(embed=msg_embed)

        if ctx.guild.voice_client is None:
            await self.join_channel(ctx)

        voice_client = ctx.guild.voice_client
        loop = asyncio.get_event_loop()
        download_path = os.path.abspath("./tmp/")
        playing_file = YouTube(video_url).streams.filter(audio_codec="opus", only_audio=True).first().download(download_path, filename=str(ctx.guild.id))
        voice_client.play(discord.FFmpegOpusAudio(playing_file, codec="copy"), after=lambda a: loop.create_task(self.next_song(ctx)))
    
    async def play(self,ctx:commands.Context, arg:str):
        loop = asyncio.get_event_loop()
        song_list = []

        if arg.find("playlist") + 1:        #We add 1 because find returns -1 if nothing is found
            playlist_id = arg[arg.find("list=") + 5 : ]
            playlist = api.get_playlist_by_id(playlist_id=playlist_id)
            if ctx.guild.voice_client.is_playing():
                playlist_name = playlist.items[0].snippet.title
                discord.Embed(
                    colour=discord.Colour.blue(),
                    description="Queued [{0}]({1})[{2}]".format(playlist_name, arg, ctx.author.mention)
                )

            pageToken = None
            while True:
                playlist_items = api.get_playlist_items(playlist_id= playlist_id, page_token=pageToken)
                await asyncio.sleep(0.1)

                for item in playlist.items:
                    song_list.append(item.contentDetails.videoId)

                pageToken = playlist_items.nextPageToken

                if pageToken is None:
                    break
        elif arg.find("watch?v=") + 1:
            if arg.find("&") + 1: #Removes additional video queries (such as list)
                arg = arg[:arg.find("&")]
            video_id = arg[arg.find("watch?v=") + 8 : ]
            song_list.append(video_id)
        else:
            video = api.search(q=arg).items[0]
            video_id = video.id.videoId
            song_list.append(video_id)  

        
        if ctx.guild.voice_client is None or not ctx.guild.voice_client.is_connected():
            self.__prepare__(ctx)
            self.__queue__(ctx.guild, song_list)
            loop.create_task(self.__do_play__(ctx))
        else:
            self.__queue__(ctx.guild, song_list)

    async def next_song(self, ctx):

        self.guild_tracks[ctx.guild.id] += 1

        if self.guild_queues[ctx.guild.id] is None:
            return
        
        if len(self.guild_queues[ctx.guild.id]) - 1 < self.guild_tracks[ctx.guild.id]:
            if self.guild_loop[ctx.guild.id] is True:
                self.guild_tracks[ctx.guild.id] = 0
            else:
                await self.leave_channel(ctx)
                return
        
        voice_client = ctx.guild.voice_client
        if voice_client.is_playing():
            video_id = self.guild_queues[ctx.guild.id][self.guild_tracks[ctx.guild.id]]
            video_url = "https://youtube.com/watch?v={0}".format(video_id)
            video_name = api.get_video_by_id(video_id=video_id).items[0].snippet.title
            msg_embed = discord.Embed(
                colour=discord.Colour.blue(),
                title="Now Playing",
                description="[{0}]({1})[{2}]".format(video_name, video_url, ctx.author.mention)
            )
            await ctx.channel.send(embed=msg_embed)

            download_path = os.path.abspath("./tmp/")
            playing_file = YouTube(video_url).streams.filter(audio_codec="opus", only_audio=True).first().download(download_path, filename=str(ctx.guild.id))
            voice_client.source = discord.FFmpegOpusAudio(playing_file, codec="copy")
        else:
            loop = asyncio.get_event_loop()
            loop.create_task(self.__do_play__(ctx))

    async def shuffle(self,ctx):
        random.shuffle(self.guild_queues[ctx.guild.id])
        await ctx.message.add_reaction("🔀")

    async def loop(self,ctx):
        self.guild_loop[ctx.guild.id] = True
        await ctx.message.add_reaction("🔄")
    
    async def show_queue(self, ctx):
        result = "```ml\n"
        track = 1
        for item in self.guild_queues[ctx.guild.id]:
            video_title = api.get_video_by_id(video_id=item).items[0].snippet.title
            await asyncio.sleep(0.1)
            result += "{0}) {1}\n".format(track,video_title)
            track += 1
        result += "```"
        await ctx.message.channel.send(result)