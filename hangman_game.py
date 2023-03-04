import discord
class hangmanButtons(discord.ui.View):
  def __init__(self, content:str, channel:discord.TextChannel, guesses:int):
    super().__init__(timeout = None)
    self.content = content
    self.letter_array = []
    self.attempts = guesses
    self.total_attempts = 0
    self.string = ""
    self.channel = channel
    self.updateString()
    
  def updateString(self):
    string = ""
    for x in self.content:
      if x.__eq__(" "):
        string += " "
      elif x.lower() in self.letter_array:
        string += x.lower()
      else:
        string += '\_'
    self.string = string
        
  async def checkGameOver(self, user:discord.User):
    if self.attempts == 0 and not (self.string.__eq__(self.content)):
      await self.channel.send(f"The host wins!\n\nThe word(s) are: {self.content}")
      self.stop()
      return True
    elif self.string.__eq__(self.content.lower()):
      await self.channel.send(f"{user.mention} wins! The word(s) are: {self.content}")
      return True
      self.stop()
    else:
      return False
      
  @discord.ui.button(label = 'A', style = discord.ButtonStyle.blurple)
  async def button1(self, interaction:discord.Interaction, button:discord.Button):
    if 'a' in self.letter_array:
      await interaction.response.defer()
    else:
      self.letter_array.append('a')
      self.updateString()
      self.checkLetter('a')
      stri = ""
      for x in self.letter_array:
        stri += f'{x}, '
      await interaction.response.edit_message(content = f'{self.string}\n\nStrikes Left: {self.attempts}\nGuessed letters: {stri[:-2]}')
      await self.checkGameOver(interaction.user)
  @discord.ui.button(label = 'B', style = discord.ButtonStyle.blurple)
  async def button2(self, interaction:discord.Interaction, button:discord.Button):
    if 'b' in self.letter_array:
      await interaction.response.defer()
    else:
      self.letter_array.append('b')
      self.updateString()
      self.checkLetter('b')
      stri = ""
      for x in self.letter_array:
        stri += f'{x}, '
      await interaction.response.edit_message(content = f'{self.string}\n\nStrikes Left: {self.attempts}\nGuessed letters: {stri[:-2]}')
      await self.checkGameOver(interaction.user)
  @discord.ui.button(label = 'C', style = discord.ButtonStyle.blurple)
  async def button3(self, interaction:discord.Interaction, button:discord.Button):
    if 'c' in self.letter_array:
      await interaction.response.defer()
    else:
      self.letter_array.append('c')
      self.updateString()
      self.checkLetter('c')
      stri = ""
      for x in self.letter_array:
        stri += f'{x}, '
      await interaction.response.edit_message(content = f'{self.string}\n\nStrikes Left: {self.attempts}\nGuessed letters: {stri[:-2]}')
      await self.checkGameOver(interaction.user)
  @discord.ui.button(label = 'D', style = discord.ButtonStyle.blurple)
  async def button4(self, interaction:discord.Interaction, button:discord.Button):
    if 'd' in self.letter_array:
      await interaction.response.defer()
    else:
      self.letter_array.append('d')
      self.updateString()
      self.checkLetter('d')
      stri = ""
      for x in self.letter_array:
        stri += f'{x}, '
      await interaction.response.edit_message(content = f'{self.string}\n\nStrikes Left: {self.attempts}\nGuessed letters: {stri[:-2]}')
      await self.checkGameOver(interaction.user)
  @discord.ui.button(label = 'E', style = discord.ButtonStyle.blurple)
  async def button5(self, interaction:discord.Interaction, button:discord.Button):
    if 'e' in self.letter_array:
      await interaction.response.defer()
    else:
      self.letter_array.append('e')
      self.updateString()
      self.checkLetter('e')
      stri = ""
      for x in self.letter_array:
        stri += f'{x}, '
      await interaction.response.edit_message(content = f'{self.string}\n\nStrikes Left: {self.attempts}\nGuessed letters: {stri[:-2]}')
      await self.checkGameOver(interaction.user)
  @discord.ui.button(label = 'F', style = discord.ButtonStyle.blurple)
  async def button6(self, interaction:discord.Interaction, button:discord.Button):
    if 'f' in self.letter_array:
      await interaction.response.defer()
    else:
      self.letter_array.append('f')
      self.updateString()
      self.checkLetter('f')
      stri = ""
      for x in self.letter_array:
        stri += f'{x}, '
      await interaction.response.edit_message(content = f'{self.string}\n\nStrikes Left: {self.attempts}\nGuessed letters: {stri[:-2]}')
      await self.checkGameOver(interaction.user)
  @discord.ui.button(label = 'G', style = discord.ButtonStyle.blurple)
  async def button7(self, interaction:discord.Interaction, button:discord.Button):
    if 'g' in self.letter_array:
      await interaction.response.defer()
    else:
      self.letter_array.append('g')
      self.updateString()
      self.checkLetter('g')
      stri = ""
      for x in self.letter_array:
        stri += f'{x}, '
      await interaction.response.edit_message(content = f'{self.string}\n\nStrikes Left: {self.attempts}\nGuessed letters: {stri[:-2]}')
      await self.checkGameOver(interaction.user)
  @discord.ui.button(label = 'H', style = discord.ButtonStyle.blurple)
  async def button8(self, interaction:discord.Interaction, button:discord.Button):
    if 'h' in self.letter_array:
      await interaction.response.defer()
    else:
      self.letter_array.append('h')
      self.updateString()
      self.checkLetter('h')
      stri = ""
      for x in self.letter_array:
        stri += f'{x}, '
      await interaction.response.edit_message(content = f'{self.string}\n\nStrikes Left: {self.attempts}\nGuessed letters: {stri[:-2]}')
      await self.checkGameOver(interaction.user)
  @discord.ui.button(label = 'I', style = discord.ButtonStyle.blurple)
  async def button9(self, interaction:discord.Interaction, button:discord.Button):
    if 'i' in self.letter_array:
      await interaction.response.defer()
    else:
      self.letter_array.append('i')
      self.updateString()
      self.checkLetter('i')
      stri = ""
      for x in self.letter_array:
        stri += f'{x}, '
      await interaction.response.edit_message(content = f'{self.string}\n\nStrikes Left: {self.attempts}\nGuessed letters: {stri[:-2]}')
      await self.checkGameOver(interaction.user)
  @discord.ui.button(label = 'J', style = discord.ButtonStyle.blurple)
  async def button10(self, interaction:discord.Interaction, button:discord.Button):
    if 'j' in self.letter_array:
      await interaction.response.defer()
    else:
      self.letter_array.append('j')
      self.updateString()
      self.checkLetter('j')
      stri = ""
      for x in self.letter_array:
        stri += f'{x}, '
      await interaction.response.edit_message(content = f'{self.string}\n\nStrikes Left: {self.attempts}\nGuessed letters: {stri[:-2]}')
      await self.checkGameOver(interaction.user)
  @discord.ui.button(label = 'K', style = discord.ButtonStyle.blurple)
  async def button11(self, interaction:discord.Interaction, button:discord.Button):
    if 'k' in self.letter_array:
      await interaction.response.defer()
    else:
      self.letter_array.append('k')
      self.updateString()
      self.checkLetter('k')
      stri = ""
      for x in self.letter_array:
        stri += f'{x}, '
      await interaction.response.edit_message(content = f'{self.string}\n\nStrikes Left: {self.attempts}\nGuessed letters: {stri[:-2]}')
      await self.checkGameOver(interaction.user)
  @discord.ui.button(label = 'L', style = discord.ButtonStyle.blurple)
  async def button12(self, interaction:discord.Interaction, button:discord.Button):
    if 'l' in self.letter_array:
      await interaction.response.defer()
    else:
      self.letter_array.append('l')
      self.updateString()
      self.checkLetter('l')
      stri = ""
      for x in self.letter_array:
        stri += f'{x}, '
      await interaction.response.edit_message(content = f'{self.string}\n\nStrikes Left: {self.attempts}\nGuessed letters: {stri[:-2]}')
      await self.checkGameOver(interaction.user)
  @discord.ui.button(label = 'M', style = discord.ButtonStyle.blurple)
  async def button13(self, interaction:discord.Interaction, button:discord.Button):
    if 'm' in self.letter_array:
      await interaction.response.defer()
    else:
      self.letter_array.append('m')
      self.updateString()
      self.checkLetter('m')
      stri = ""
      for x in self.letter_array:
        stri += f'{x}, '
      await interaction.response.edit_message(content = f'{self.string}\n\nStrikes Left: {self.attempts}\nGuessed letters: {stri[:-2]}')
      await self.checkGameOver(interaction.user)
  @discord.ui.button(label = 'N', style = discord.ButtonStyle.blurple)
  async def button14(self, interaction:discord.Interaction, button:discord.Button):
    if 'n' in self.letter_array:
      await interaction.response.defer()
    else:
      self.letter_array.append('n')
      self.updateString()
      self.checkLetter('n')
      stri = ""
      for x in self.letter_array:
        stri += f'{x}, '
      await interaction.response.edit_message(content = f'{self.string}\n\nStrikes Left: {self.attempts}\nGuessed letters: {stri[:-2]}')
      await self.checkGameOver(interaction.user)
  @discord.ui.button(label = 'O', style = discord.ButtonStyle.blurple)
  async def button15(self, interaction:discord.Interaction, button:discord.Button):
    if 'o' in self.letter_array:
      await interaction.response.defer()
    else:
      self.letter_array.append('o')
      self.updateString()
      self.checkLetter('o')
      stri = ""
      for x in self.letter_array:
        stri += f'{x}, '
      await interaction.response.edit_message(content = f'{self.string}\n\nStrikes Left: {self.attempts}\nGuessed letters: {stri[:-2]}')
      await self.checkGameOver(interaction.user)
  @discord.ui.button(label = 'P', style = discord.ButtonStyle.blurple)
  async def button16(self, interaction:discord.Interaction, button:discord.Button):
    if 'p' in self.letter_array:
      await interaction.response.defer()
    else:
      self.letter_array.append('p')
      self.updateString()
      self.checkLetter('p')
      stri = ""
      for x in self.letter_array:
        stri += f'{x}, '
      await interaction.response.edit_message(content = f'{self.string}\n\nStrikes Left: {self.attempts}\nGuessed letters: {stri[:-2]}')
      await self.checkGameOver(interaction.user)
  @discord.ui.button(label = 'Q', style = discord.ButtonStyle.blurple)
  async def button17(self, interaction:discord.Interaction, button:discord.Button):
    if 'q' in self.letter_array:
      await interaction.response.defer()
    else:
      self.letter_array.append('q')
      self.updateString()
      self.checkLetter('q')
      stri = ""
      for x in self.letter_array:
        stri += f'{x}, '
      await interaction.response.edit_message(content = f'{self.string}\n\nStrikes Left: {self.attempts}\nGuessed letters: {stri[:-2]}')
      await self.checkGameOver(interaction.user)
  @discord.ui.button(label = 'R', style = discord.ButtonStyle.blurple)
  async def button18(self, interaction:discord.Interaction, button:discord.Button):
    if 'r' in self.letter_array:
      await interaction.response.defer()
    else:
      self.letter_array.append('r')
      self.updateString()
      self.checkLetter('r')
      stri = ""
      for x in self.letter_array:
        stri += f'{x}, '
      await interaction.response.edit_message(content = f'{self.string}\n\nStrikes Left: {self.attempts}\nGuessed letters: {stri[:-2]}')
      await self.checkGameOver(interaction.user)
  @discord.ui.button(label = 'S', style = discord.ButtonStyle.blurple)
  async def button19(self, interaction:discord.Interaction, button:discord.Button):
    if 's' in self.letter_array:
      await interaction.response.defer()
    else:
      self.letter_array.append('s')
      self.updateString()
      self.checkLetter('s')
      stri = ""
      for x in self.letter_array:
        stri += f'{x}, '
      await interaction.response.edit_message(content = f'{self.string}\n\nStrikes Left: {self.attempts}\nGuessed letters: {stri[:-2]}')
      await self.checkGameOver(interaction.user)
  @discord.ui.button(label = 'T', style = discord.ButtonStyle.blurple)
  async def button20(self, interaction:discord.Interaction, button:discord.Button):
    if 't' in self.letter_array:
      await interaction.response.defer()
    else:
      self.letter_array.append('t')
      self.updateString()
      self.checkLetter('t')
      stri = ""
      for x in self.letter_array:
        stri += f'{x}, '
      await interaction.response.edit_message(content = f'{self.string}\n\nStrikes Left: {self.attempts}\nGuessed letters: {stri[:-2]}')
      await self.checkGameOver(interaction.user)
  @discord.ui.button(label = 'U', style = discord.ButtonStyle.blurple)
  async def button21(self, interaction:discord.Interaction, button:discord.Button):
    if 'u' in self.letter_array:
      await interaction.response.defer()
    else:
      self.letter_array.append('u')
      self.updateString()
      self.checkLetter('u')
      stri = ""
      for x in self.letter_array:
        stri += f'{x}, '
      await interaction.response.edit_message(content = f'{self.string}\n\nStrikes Left: {self.attempts}\nGuessed letters: {stri[:-2]}')
      await self.checkGameOver(interaction.user)
  @discord.ui.button(label = 'V/X', style = discord.ButtonStyle.blurple)
  async def button22(self, interaction:discord.Interaction, button:discord.Button):
    if 'v' in self.letter_array:
      await interaction.response.defer()
    else:
      self.letter_array.append('v')
      self.letter_array.append('x')
      self.updateString()
      check = False
      for x in self.content:
        if x.lower().__eq__('x') or x.lower().__eq__('v'):
          check = True
      if not check:
        self.attempts -= 1
      stri = ""
      for x in self.letter_array:
        stri += f'{x}, '
      await interaction.response.edit_message(content = f'{self.string}\n\nStrikes Left: {self.attempts}\nGuessed letters: {stri[:-2]}')
      await self.checkGameOver(interaction.user)
  @discord.ui.button(label = 'W', style = discord.ButtonStyle.blurple)
  async def button23(self, interaction:discord.Interaction, button:discord.Button):
    if 'w' in self.letter_array:
      await interaction.response.defer()
    else:
      self.letter_array.append('w')
      self.updateString()
      self.checkLetter('w')
      stri = ""
      for x in self.letter_array:
        stri += f'{x}, '
      await interaction.response.edit_message(content = f'{self.string}\n\nStrikes Left: {self.attempts}\nGuessed letters: {stri[:-2]}')
      await self.checkGameOver(interaction.user)
  @discord.ui.button(label = 'Y', style = discord.ButtonStyle.blurple)
  async def button24(self, interaction:discord.Interaction, button:discord.Button):
    if 'y' in self.letter_array:
      await interaction.response.defer()
    else:
      self.letter_array.append('y')
      self.updateString()
      self.checkLetter('y')
      stri = ""
      for x in self.letter_array:
        stri += f'{x}, '
      await interaction.response.edit_message(content = f'{self.string}\n\nStrikes Left: {self.attempts}\nGuessed letters: {stri[:-2]}')
      await self.checkGameOver(interaction.user)
  @discord.ui.button(label = 'Z', style = discord.ButtonStyle.blurple)
  async def button25(self, interaction:discord.Interaction, button:discord.Button):
    if 'z' in self.letter_array:
      await interaction.response.defer()
    else:
      self.letter_array.append('z')
      self.updateString()
      self.checkLetter('z')
      stri = ""
      for x in self.letter_array:
        stri += f'{x}, '
      await interaction.response.edit_message(content = f'{self.string}\n\nStrikes Left: {self.attempts}\nGuessed letters: {stri[:-2]}')
      await self.checkGameOver(interaction.user)
        
  def checkLetter(self, letter):
    flag = False
    for x in self.content.lower():
      if x.__eq__(letter):
        flag = True
    if not flag:
      self.attempts = self.attempts - 1