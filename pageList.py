import discord

class page:
  def __init__(self, title, text, head, tail):
    self.value = 0
    self.title = title
    self.text = text
    self.head = head
    self.tail = tail
    if isinstance(text, list):
      self.num_pages = len(text)
    else:
      self.num_pages = 1
    
  def __str__(self):
    string = f"{self.title}\n"
    if isinstance(self.text, list):
      for x in self.text:
        if x == self.text[len(self.text) - 1]:
          string += f"{x}"
        else:
          string += f"{x}\n"
    else:
      string += f"{self.text}"
    return string

class pageList:
  def __init__(self):
    self.value = 0
    self.cursor = None
    self.size = 0
    self.head = None
    self.tail = None
    
  def addBefore(self, title, text):
    if self.size == 0:
      node = page(title, text, None, None)
      self.head = node
      self.tail = node
      self.cursor = node
    elif self.cursor == None:
      node = page(title, text, None, self.head)
      self.head.head = node
      self.head = node
      self.cursor = node
    else:
      if self.cursor == self.head:
        node = page(title, text, None, self.head)
        self.head.head = node
        self.head = node
        self.cursor = node
      else:
        node = page(title, text, self.cursor.head, self.cursor)
        self.cursor.head.tail = node
        self.cursor.head = node
        self.cursor = node
    self.size += 1
    
  def addAfter(self, title, text):
    if self.size == 0:
      node = page(title, text, None, None)
      self.head = node
      self.tail = node
      self.cursor = node
    elif self.cursor == None:
      node = page(title, text, self.head, None)
      self.head.tail = node
      self.tail = node
      self.cursor = node
    else:
      if self.cursor == self.tail:
        node = page(title, text, self.cursor, None)
        self.cursor.tail = node
        self.cursor = node
        self.tail = node
      else:
        node = page(title, text, self.cursor, self.cursor.tail)
        self.cursor.tail.head = node
        self.cursor.tail = node
        self.cursor = node
    self.size += 1  
  def next(self):
    if self.cursor == None:
      return
    else:
      self.cursor = self.cursor.tail   
      
  def back(self):
    if self.cursor == None:
      return
    else:
      self.cursor = self.cursor.head  
        
  def view(self):
    node = self.head
    while node != None:
      print(node)
      node = node.tail
  
  def getTitle(self): 
    if self.cursor == None:
      return None
    else:
      return self.cursor.title
        
  def isCurrent(self):
    return self.cursor != None
  
  def getText(self):
    if self.cursor == None:
      return None
    else:
      return self.cursor.text
    
class buttonMenu(discord.ui.View):
  def __init__(self, array:pageList):
    super().__init__(timeout = None)
    self.value = 0
    self.list = array
    self.embed_list = embedList(array)
    self.cursor = 0
  @discord.ui.button(label = "<--", style = discord.ButtonStyle.grey)
  async def button1(self, interaction:discord.Interaction, button: discord.ui.Button):
    if self.cursor != 0:
      self.cursor -= 1
      await interaction.response.edit_message(embed = self.embed_list[self.cursor])
    else:
      await interaction.response.defer()
  @discord.ui.button(label = "-->", style = discord.ButtonStyle.grey)
  async def button2(self, interaction:discord.Interaction, button: discord.ui.Button):
    if self.cursor != len(self.embed_list) - 1:
      self.cursor += 1
      await interaction.response.edit_message(embed = self.embed_list[self.cursor])
    else:
      await interaction.response.defer()
  def display(self):
    return self.embed_list[self.cursor]
def embedList(text:pageList):
  embedList = []
  node = text.head
  while node != None:
    if isinstance(node.text, list):
      for i in node.text:
        embedList.append(discord.Embed(title = node.title, description = i))
    else:
      embedList.append(discord.Embed(title = node.title, description = node.text))
    node = node.tail
  return embedList



