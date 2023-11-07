import random
import discord
NUMBER_OF_HEROES = 36
HEROES = ['D.VA', 'Junker Queen', 'Orisa', 'Reinhardt', 'Roadhog', 'Sigma', 'Winston', 'Zarya', 'Doomfist','Rammattra', 'Wrecking Ball', 'Ashe', 'Bastion', 'Cassidy', 'Echo', 'Genji', 'Hanzo', 'Junkrat', 'Mei', 'Pharah', 'Reaper', 'Sojourn', 'Soldier 76', 'Sombra', 'Symmetra', 'Torbjörn', 'Tracer', 'Widowmaker', 'Ana', 'Baptiste', 'Brigitte', 'Kiriko', 'Lúcio', 'Mercy', 'Moira', 'Zenyatta']
TANK = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
DPS = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
SUPPORT = [28, 29, 30, 31, 32, 33, 34, 35]

def getRandomHero(role = ""):
  if role.__eq__(""):
    return EMBEDS[random.randint(0, NUMBER_OF_HEROES - 1)]
  elif ('good') in str(role).lower() and ('tank') in str(role).lower():
    return EMBEDS[random.randint(0,9)]
  elif ('tank') in str(role).lower():
    return EMBEDS[random.randint(0,10)]
  elif ('dps') in str(role).lower() or ('damage') in str(role).lower():
    return EMBEDS[random.randint(11, 27)]
  elif ('support') in str(role).lower() or "healer" in str(role).lower():
    return EMBEDS[random.randint(28, 35)]
  return None


DVA_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1064814315921756160/9k.png"
JUNKER_QUEEN_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1064814667316350976/images.png"
ORISA_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1064814507916021782/Z.png"
RAMATTRA_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1064814730163793920/Z.png"
REINHARDT_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1064814883281047612/images.png"
ROADHOG_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1064815083030577234/images.png"
SIGMA_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1064814969792766052/images.png"
WINSTON_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1064814816423858256/images.png"
ZARYA_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1064815213423120434/Z.png"
DOOMFIST_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1064814421060374549/images.png"
WRECKING_BALL_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1064815156825182258/2Q.png"
ASHE_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1064812631514427493/9k.png"
BASTION_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1064812689412595712/2Q.png"
CASSIDY_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1064812750297104444/2Q.png"
ECHO_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1064812886100295740/images.png"
GENJI_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1064812939841900625/Z.png"
HANZO_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1064812991289241651/9k.png"
JUNKRAT_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1064813034637361172/Z.png"
MEI_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1064813188887101450/images.png"
PHARAH_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1064813262971093022/Z.png"
REAPER_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1064813418978230292/images.png"
SOJOURN_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1064813814215872522/9k.png"
SOLDIER_76_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1064813736260538388/images.png"
SOMBRA_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1064813889407168522/images.png"
SYMMETRA_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1064813975109382154/2Q.png"
TORBJORN_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1064814049747013672/2Q.png"
TRACER_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1064814117992546314/9k.png"
WIDOWMAKER_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1064814266428960768/images.png"
ANA_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1064811806813585439/Z.png"
BAPTISTE_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1064811964464906250/images.png"
BRIGITTE_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1064812128298614874/9k.png"
KIRIKO_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1064812448198176798/images.png"
LUCIO_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1064812549960368238/images.png"
MERCY_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1064812042181165067/9k.png"
MOIRA_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1064812259722919986/images.png"
ZENYATTA_LINK = "https://cdn.discordapp.com/attachments/1064811650298949642/1064817275984695336/images.png"
DVA = discord.Embed(
    title = "D.VA",
    colour = discord.Colour.red()
)
DVA.set_footer(text = "~~Overwatch Hero Generator~~")
DVA.set_image(url = DVA_LINK)
DVA.set_author(name = 'OW', icon_url = "https://cdn.discordapp.com/attachments/1035790494199984191/1047619206927089746/unknown.png")
JUNKER_QUEEN = discord.Embed(
    title = "Junker Queen",
    colour = discord.Colour.red()
)
JUNKER_QUEEN.set_footer(text = "~~Overwatch Hero Generator~~")
JUNKER_QUEEN.set_image(url = JUNKER_QUEEN_LINK)
ORISA = discord.Embed(
    title = "Orisa",
    colour = discord.Colour.red()
)
ORISA.set_footer(text = "~~Overwatch Hero Generator~~")
ORISA.set_image(url = ORISA_LINK)
RAMATTRA = discord.Embed(
	title = "Ramattra", 
	colour = discord.Colour.red()
)
RAMATTRA.set_footer(text = "~~Overwatch Hero Generator~~")
RAMATTRA.set_image(url = RAMATTRA_LINK)
REINHARDT = discord.Embed(
    title = "Reinhardt",
    colour = discord.Colour.red()
)
REINHARDT.set_footer(text = "~~Overwatch Hero Generator~~")
REINHARDT.set_image(url = REINHARDT_LINK)
ROADHOG = discord.Embed(
    title = "Roadhog",
    colour = discord.Colour.red()
)
ROADHOG.set_footer(text = "~~Overwatch Hero Generator~~")
ROADHOG.set_image(url = ROADHOG_LINK)
SIGMA = discord.Embed(
    title = "Sigma",
    colour = discord.Colour.red()
)
SIGMA.set_footer(text = "~~Overwatch Hero Generator~~")
SIGMA.set_image(url = SIGMA_LINK)
WINSTON = discord.Embed(
    title = "Winston",
    colour = discord.Colour.red()
)
WINSTON.set_footer(text = "~~Overwatch Hero Generator~~")
WINSTON.set_image(url = WINSTON_LINK)
ZARYA = discord.Embed(
    title = "Zarya",
    colour = discord.Colour.red()
)
ZARYA.set_footer(text = "~~Overwatch Hero Generator~~")
ZARYA.set_image(url = ZARYA_LINK)
DOOMFIST = discord.Embed(
    title = "Doomfist",
    colour = discord.Colour.red()
)
DOOMFIST.set_footer(text = "~~Overwatch Hero Generator~~")
DOOMFIST.set_image(url = DOOMFIST_LINK)
WRECKING_BALL = discord.Embed(
    title = "Wrecking Ball",
    colour = discord.Colour.red()
)
WRECKING_BALL.set_footer(text = "~~Overwatch Hero Generator~~")
WRECKING_BALL.set_image(url = WRECKING_BALL_LINK)
ASHE = discord.Embed(
    title = "Ashe",
    colour = discord.Colour.red()
)
ASHE.set_footer(text = "~~Overwatch Hero Generator~~")
ASHE.set_image(url = ASHE_LINK)
BASTION = discord.Embed(
    title = "Bastion",
    colour = discord.Colour.red()
)
BASTION.set_footer(text = "~~Overwatch Hero Generator~~")
BASTION.set_image(url = BASTION_LINK)
CASSIDY = discord.Embed(
    title = "Cassidy",
    colour = discord.Colour.red()
)
CASSIDY.set_footer(text = "~~Overwatch Hero Generator~~")
CASSIDY.set_image(url = CASSIDY_LINK)
ECHO = discord.Embed(
    title = "Echo",
    colour = discord.Colour.red()
)
ECHO.set_footer(text = "~~Overwatch Hero Generator~~")
ECHO.set_image(url = ECHO_LINK)
GENJI = discord.Embed(
    title = "Genji",
    colour = discord.Colour.red()
)
GENJI.set_footer(text = "~~Overwatch Hero Generator~~")
GENJI.set_image(url = GENJI_LINK)
HANZO = discord.Embed(
    title = "Hanzo",
    colour = discord.Colour.red()
)
HANZO.set_footer(text = "~~Overwatch Hero Generator~~")
HANZO.set_image(url = HANZO_LINK)
JUNKRAT = discord.Embed(
    title = "Junkrat",
    colour = discord.Colour.red()
)
JUNKRAT.set_footer(text = "~~Overwatch Hero Generator~~")
JUNKRAT.set_image(url = JUNKRAT_LINK)
MEI = discord.Embed(
    title = "Mei",
    colour = discord.Colour.red()
)
MEI.set_footer(text = "~~Overwatch Hero Generator~~")
MEI.set_image(url = MEI_LINK)
PHARAH = discord.Embed(
    title = "Pharah",
    colour = discord.Colour.red()
)
PHARAH.set_footer(text = "~~Overwatch Hero Generator~~")
PHARAH.set_image(url = PHARAH_LINK)
REAPER = discord.Embed(
    title = "Reaper",
    colour = discord.Colour.red()
)
REAPER.set_footer(text = "~~Overwatch Hero Generator~~")
REAPER.set_image(url = REAPER_LINK)
SOJOURN = discord.Embed(
    title = "Sojourn",
    colour = discord.Colour.red()
)
SOJOURN.set_footer(text = "~~Overwatch Hero Generator~~")
SOJOURN.set_image(url = SOJOURN_LINK)
SOLDIER_76 = discord.Embed(
    title = "Soldier 76",
    colour = discord.Colour.red()
)
SOLDIER_76.set_footer(text = "~~Overwatch Hero Generator~~")
SOLDIER_76.set_image(url = SOLDIER_76_LINK)
SOMBRA = discord.Embed(
    title = "Sombra",
    colour = discord.Colour.red()
)
SOMBRA.set_footer(text = "~~Overwatch Hero Generator~~")
SOMBRA.set_image(url = SOMBRA_LINK)
SYMMETRA = discord.Embed(
    title = "Symmetra",
    colour = discord.Colour.red()
)
SYMMETRA.set_footer(text = "~~Overwatch Hero Generator~~")
SYMMETRA.set_image(url = SYMMETRA_LINK)
TORBJORN = discord.Embed(
    title = "Torbjörn",
    colour = discord.Colour.red()
)
TORBJORN.set_footer(text = "~~Overwatch Hero Generator~~")
TORBJORN.set_image(url = TORBJORN_LINK)
TRACER = discord.Embed(
    title = "Tracer",
    colour = discord.Colour.red()
)
TRACER.set_footer(text = "~~Overwatch Hero Generator~~")
TRACER.set_image(url = TRACER_LINK)
WIDOWMAKER = discord.Embed(
    title = "Widowmaker",
    colour = discord.Colour.red()
)
WIDOWMAKER.set_footer(text = "~~Overwatch Hero Generator~~")
WIDOWMAKER.set_image(url = WIDOWMAKER_LINK)
ANA = discord.Embed(
    title = "Ana",
    colour = discord.Colour.red()
)
ANA.set_footer(text = "~~Overwatch Hero Generator~~")
ANA.set_image(url = ANA_LINK)
BAPTISTE = discord.Embed(
    title = "Baptiste",
    colour = discord.Colour.red()
)
BAPTISTE.set_footer(text = "~~Overwatch Hero Generator~~")
BAPTISTE.set_image(url = BAPTISTE_LINK)
BRIGITTE = discord.Embed(
    title = "Brigitte",
    colour = discord.Colour.red()
)
BRIGITTE.set_footer(text = "~~Overwatch Hero Generator~~")
BRIGITTE.set_image(url = BRIGITTE_LINK)
KIRIKO = discord.Embed(
    title = "Kiriko",
    colour = discord.Colour.red()
)
KIRIKO.set_footer(text = "~~Overwatch Hero Generator~~")
KIRIKO.set_image(url = KIRIKO_LINK)
LUCIO = discord.Embed(
    title = "Lúcio",
    colour = discord.Colour.red()
)
LUCIO.set_footer(text = "~~Overwatch Hero Generator~~")
LUCIO.set_image(url = LUCIO_LINK)
MERCY = discord.Embed(
    title = "Mercy",
    colour = discord.Colour.red()
)
MERCY.set_footer(text = "~~Overwatch Hero Generator~~")
MERCY.set_image(url = MERCY_LINK)
MOIRA = discord.Embed(
    title = "Moira",
    colour = discord.Colour.red()
)
MOIRA.set_footer(text = "~~Overwatch Hero Generator~~")
MOIRA.set_image(url = MOIRA_LINK)
ZENYATTA = discord.Embed(
    title = "Zenyatta",
    colour = discord.Colour.red()
)
ZENYATTA.set_footer(text = "~~Overwatch Hero Generator~~")
ZENYATTA.set_image(url = ZENYATTA_LINK)
EMBEDS = [DVA, JUNKER_QUEEN, ORISA, REINHARDT, ROADHOG, SIGMA, WINSTON, ZARYA, DOOMFIST, RAMATTRA, WRECKING_BALL, ASHE, BASTION, CASSIDY, ECHO, GENJI, HANZO, JUNKRAT, MEI, PHARAH, REAPER, SOJOURN, SOLDIER_76, SOMBRA, SYMMETRA, TORBJORN, TRACER, WIDOWMAKER, ANA, BAPTISTE, BRIGITTE, KIRIKO, LUCIO, MERCY, MOIRA, ZENYATTA]
