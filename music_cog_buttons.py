from ast import alias
import discord
from discord.ext import commands
from discord import app_commands
from yt_dlp import YoutubeDL

class music_cog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    
    #all the music related stuff
    self.is_playing = False
    self.is_paused = False
	
    # 2d array containing [song, channel]
    self.music_queue = []
    self.post_list = []
    self.YDL_OPTIONS = {'format': 'bestaudio','outtmpl':'%(extractor)s-%(id)s-%(title)s.%(ext)s', 'noplaylist':'True', 'source_address': '0.0.0.0'}
    self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    self.message = None
    self.vc = None
  #searching the item on youtube
  def search_yt(self, item):
    with YoutubeDL(self.YDL_OPTIONS) as ydl:
      try: 
        info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
      except Exception: 
        return False
    return {'source': info['url'], 'title': info['title']}

  def play_next(self):
    if len(self.music_queue) > 0:
      self.is_playing = True
            #get the first url
      m_url = self.music_queue[0][0]['source']
            #remove the first element as you are currently playing it
      self.music_queue.pop(0)
      self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
    else:
      self.is_playing = False


    # infinite loop checking 
  async def play_music(self, ctx):
    if len(self.music_queue) > 0:
      self.is_playing = True
      m_url = self.music_queue[0][0]['source']
            #try to connect to voice channel if you are not already connected
      if self.vc == None or not self.vc.is_connected():
        self.vc = await self.music_queue[0][1].connect()
                #in case we fail to connect
        if self.vc == None:
          await ctx.channel.send("Could not connect to the voice channel")
          return
        else:
          await self.vc.move_to(self.music_queue[0][1])
            #remove the first element as you are currently playing it
      self.music_queue.pop(0)
      self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after= lambda e: self.play_next())
    else:
      self.is_playing = False
    
  async def update_post(self):
    if self.message != None:
      retval = "**Queued Songs:\n**"
      for i in range(0, len(self.music_queue)):
            # display a max of 5 songs in the current queue
        if (i > 4): break
        retval += self.music_queue[i][0]['title'] + "\n"
      embed = discord.Embed(title = "DJ Control Panel", description = retval, color = discord.Colour.blue())
      await self.message.edit(embed = embed)
    
  @app_commands.command(name="play", description="Plays a selected song from youtube")
  async def play(self, interaction:discord.Interaction, music:str):
    await interaction.response.defer(ephemeral = True)
    voice_channel = interaction.user.voice.channel
    if voice_channel is None:
    #you need to be connected so that the bot knows where to go
      await interaction.followup.send("Connect to a voice channel!")
    else:
      song = self.search_yt(music)
      if type(song) == type(True):
        await interaction.followup.send("Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format.")
      else:
        self.music_queue.append([song, voice_channel])
        if self.message == None:
          embed = discord.Embed(title = "DJ Control Panel", description = f"**Queued Songs:**", color = discord.Colour.blue())
          view = musicButtons(self)
          self.message = await interaction.channel.send(embed = embed, view = view)
        else:
          await self.update_post()
        if self.is_playing == False:
          await self.play_music(interaction)
        await interaction.followup.send("Song has been added.")

  @app_commands.command(name="clear", description ="Stops the music and clears the queue")
  async def clear(self, interaction:discord.Interaction):
    if self.vc != None and self.is_playing:
      self.vc.stop()
      self.music_queue = []
      await self.update_post()
    await interaction.response.send("Music queue cleared", ephemeral = True)

  @app_commands.command(name = "leave", description = "Disconnects the bot from the vc")
  async def dc(self, interaction:discord.Interaction):
    self.is_playing = False 
    self.is_paused = False
    self.music_queue = []
    await self.update_post()
    await self.vc.disconnect()
    await interaction.response.send("Bot has been disconnected", ephermeral = True)
    
class musicButtons(discord.ui.View):
  def __init__(self, cog):
    super().__init__(timeout = None)
    self.cog = cog
  @discord.ui.button(label = "◻️", style = discord.ButtonStyle.blurple)
  async def pause(self, interaction:discord.Interaction, button:discord.ui.Button):
    if self.cog.is_playing:
      self.cog.is_playing = False
      self.cog.is_paused = True
      self.cog.vc.pause()
    elif self.cog.is_paused:
      self.cog.is_paused = False
      self.cog.is_playing = True
      self.cog.vc.resume()
    await interaction.response.defer()
  @discord.ui.button(label = "⏩", style = discord.ButtonStyle.blurple)
  async def skip(self, interaction:discord.Interaction, button:discord.ui.Button):
    if self.cog.vc != None and self.cog.vc:
      self.cog.vc.stop()
      #try to play next in the queue if it exists
      await self.cog.play_music(interaction)
      await self.cog.update_post()
      await interaction.response.defer()