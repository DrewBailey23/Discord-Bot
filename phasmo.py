import random
import discord

MAPS = [
  "Bleasedale Farmhouse", "Camp Woodwind", "42 Edgefield Road",
  "Grafton Farmhouse", "10 Ridgeview Court", "Sunny Meadows (Restricted)",
  "6 Tanglewood Drive", "13 Willow Street", "Brownstone High School",
  "Maple Lodge Campsite", "Prison", "Sunny Meadows"
]

NUMBER_OF_MAPS = 12

SMALL = [
  0, 1, 2, 3, 4, 5, 6, 7
]
MEDIUM = [8, 9, 10]
LARGE = [11]

##Links for images##

TANGLEWOOD_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1066437554519416954/2Q.png"
BLEASEDALE_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1066437678972805241/2Q.png"
WOODWIND_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1066437799760363560/2Q.png"
EDGEFIELD_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1066437894815883365/Z.png"
GRAFTON_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1066438056036552714/2Q.png"
RIDGEVIEW_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1066438182234755162/9k.png"
SUNNYRES_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1066438328393666701/images.png"
WILLOW_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1066438464482058352/images.png"
HIGHSCHOOL_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1066438540092776579/Z.png"
PRISON_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1066438870650077214/2Q.png"
CAMPSITE_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1066438973418909816/2Q.png"
SUNNY_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1066439247143387177/images.png"
##Embeds for random selection##
      
TANGLEWOOD = discord.Embed(
    title = "6 Tanglewood Drive",
    colour = discord.Colour.green()
)
TANGLEWOOD.set_footer(text = "~~Phasmophobia Map Generator~~")
TANGLEWOOD.set_image(url = TANGLEWOOD_LINK)
BLEASEDALE = discord.Embed(
    title = "Bleasedale Farmhouse",
    colour = discord.Colour.green()
)
BLEASEDALE.set_footer(text = "~~Phasmophobia Map Generator~~")
BLEASEDALE.set_image(url = BLEASEDALE_LINK)
WOODWIND = discord.Embed(
    title = "Camp Woodwind",
    colour = discord.Colour.green()
)
WOODWIND.set_footer(text = "~~Phasmophobia Map Generator~~")
WOODWIND.set_image(url = WOODWIND_LINK)
EDGEFIELD = discord.Embed(
    title = "42 Edgefield Road",
    colour = discord.Colour.green()
)
EDGEFIELD.set_footer(text = "~~Phasmophobia Map Generator~~")
EDGEFIELD.set_image(url = EDGEFIELD_LINK)
GRAFTON = discord.Embed(
    title = "Grafton Farmhouse",
    colour = discord.Colour.green()
)
GRAFTON.set_footer(text = "~~Phasmophobia Map Generator~~")
GRAFTON.set_image(url = GRAFTON_LINK)
RIDGEVIEW = discord.Embed(
    title = "10 Ridgeview Court",
    colour = discord.Colour.green()
)
RIDGEVIEW.set_footer(text = "~~Phasmophobia Map Generator~~")
RIDGEVIEW.set_image(url = RIDGEVIEW_LINK)
WILLOW = discord.Embed(
    title = "13 Willow Street",
    colour = discord.Colour.green()
)
WILLOW.set_footer(text = "~~Phasmophobia Map Generator~~")
WILLOW.set_image(url = WILLOW_LINK)
HIGHSCHOOL = discord.Embed(
    title = "Brownstone High School",
    colour = discord.Colour.blue()
)
HIGHSCHOOL.set_footer(text = "~~Phasmophobia Map Generator~~")
HIGHSCHOOL.set_image(url = HIGHSCHOOL_LINK)
SUNNYRES = discord.Embed(
    title = "Sunny Meadows (Restricted)",
    colour = discord.Colour.green()
)
SUNNYRES.set_footer(text = "~~Phasmophobia Map Generator~~")
SUNNYRES.set_image(url = SUNNYRES_LINK)
CAMPSITE = discord.Embed(
    title = "Maple Lodge Campsite",
    colour = discord.Colour.blue()
)
CAMPSITE.set_footer(text = "~~Phasmophobia Map Generator~~")
CAMPSITE.set_image(url = CAMPSITE_LINK)
PRISON = discord.Embed(
    title = "Prison",
    colour = discord.Colour.blue()
)
PRISON.set_footer(text = "~~Phasmophobia Map Generator~~")
PRISON.set_image(url = PRISON_LINK)
SUNNY = discord.Embed(
    title = "Sunny Meadows",
    colour = discord.Colour.red()
)
SUNNY.set_footer(text = "~~Phasmophobia Map Generator~~")
SUNNY.set_image(url = SUNNY_LINK)
EMBEDS = [BLEASEDALE, WOODWIND, EDGEFIELD, GRAFTON, RIDGEVIEW, SUNNYRES, TANGLEWOOD, WILLOW, HIGHSCHOOL, CAMPSITE, PRISON, SUNNY]

def getEmbed(size = ""):
  if size.__eq__(""):
    return EMBEDS[random.randint(0, NUMBER_OF_MAPS - 1)]
  if 'no' in str(size).lower() or 'not' in str(size).lower():
    flag = False
    num = 0
    while not flag:
      flag = True
      num = random.randint(0, NUMBER_OF_MAPS - 1)
      if'small' in str(size).lower():
        if num in SMALL:
          flag = False
      if 'medium' in str(size).lower():
        if num in MEDIUM:
          flag = False
      if 'large' in str(size).lower():
          if num in LARGE:
            flag = False
    return EMBEDS[num]
  elif (not 'no' in str(size) or 'not' in str(size)) and 'small' in str(size).lower() or 'medium' in str(size).lower() or 'large' in str(size).lower() or 'big' in str(size).lower():
    flag = False
    num = 0
    while not flag:
      num = random.randint(0, NUMBER_OF_MAPS - 1)
      if'small' in str(size).lower():
        if num in SMALL:
          flag = True
      if 'medium' in str(size).lower():
        if num in MEDIUM:
          flag = True
      if 'large' in str(size).lower() or 'big' in str(size).lower():
          if num in LARGE:
            flag = True
    return EMBEDS[num]
  return None