import random
import discord
from datetime import datetime
from datetime import date
from discord.ext import commands
from discord import app_commands
import pageList
import phasmo
import overwatch
import valorant
import mysql.connector
from pytz import timezone

USER = ##MySQL User string
PASSWORD = ##MySQL password string
HOST = ##MySQL host string
DATABASE = ##MySQL database string

TOKEN = ##Discord Client Token

##-----------------------------------------------------------Bot Object-------------------------------------------------------------------------------
class PersistentViewBot(commands.Bot):
  def __init__(self):
    intents = discord.Intents.all()
    intents.message_content = True
    intents.members = True
    intents.presences = True
    allowed_mentions = discord.AllowedMentions.all()
    allowed_mentions.everyone = True
    super().__init__(command_prefix=commands.when_mentioned_or('.'), intents=intents, allowed_mentions = allowed_mentions)
    self.reaction_list = [] ##List of guilds with a reaction channel, so there's no need to query data if there's no reaction post.
    self.level_list = [] ##List of guilds with enabled notifications.
    self.mod_channels = [] ##List of [guild_id, channel_id] for moderation channels.
    self.stalk_list = [] ##List of [user to notify, user to check] for the stalk command.
    
  async def setup_hook(self) -> None:
    # Register the persistent view for listening here.
    # Note that this does not send the view to any message.
    # In order to do this you need to first send a message with the View, which is shown below.
    self.add_view(roles2())
    self.add_view(pronounButtons())
    
  ## Syncs tree commands and initializes all necessary channel lists from MySQL
  async def on_ready(self): 
    synced = await bot.tree.sync()
    con = mysql.connector.connect(user = USER, password = PASSWORD, 
                                  host = HOST, database = DATABASE)
    cursor = con.cursor()
    cursor.execute("select * from reaction_messages")
    for i in cursor:
      self.reaction_list.append(int(i[0]))
    cursor.execute("select * from level_guilds")
    for i in cursor:
      self.level_list.append(int(i[0]))
    cursor.execute("select * from mod_channels")
    for i in cursor:
      self.mod_channels.append([int(i[0]), int(i[1])])
    cursor.execute("select * from stalker_table")
    for i in cursor:
      self.stalk_list.append([int(i[1]), int(i[2]), int(i[3])])
    con.close()
    print(f'Logged in as {self.user} (ID: {self.user.id})')
    print(f"Slash Commands: {len(synced)}")
    print('------')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for /help"))

bot = PersistentViewBot()

#-------------------------------------------------------------Context Menu Commands---------------------------------------------------------

##Can only be used after making a mod channel, send a message containing who reported the message, the author, the contents of the message and the time it was reported.
@bot.tree.context_menu(name = "Report Message")
async def report_message(interaction:discord.Interaction, message:discord.Message):
  def search():
    for i in bot.mod_channels:
      if i[0] == interaction.guild_id:
        return i[1]
    return None
  channel = bot.get_channel(search())
  if channel != None:
    tz = timezone('EST')
    await channel.send(f"{interaction.user.display_name} reported {message.author.display_name}'s post at {str(datetime.now(tz))[:16]}: \"{message.content}\"")
    await interaction.response.send_message(f"You have successfully reported {message.author.display_name}'s message.", ephemeral = True)
  else:
    await interaction.response.send_message("There is not a moderator channel set up in your server. Contact an admin to use /create_mod_channel to report messages.", ephemeral = True)

#Allows users to receive notifications when someone comes online.
@bot.tree.context_menu(name = "Stalk")
async def track_user(interaction:discord.Interaction, user:discord.User):
  await interaction.response.defer(ephemeral = True)
  con = mysql.connector.connect(user = USER, database = DATABASE, 
                               host = HOST, password = PASSWORD)
  cursor = con.cursor()
  query = f"insert into stalker_table values (\"{interaction.user.id}/{user.id}/{interaction.guild.id}\", {interaction.user.id}, {user.id}, {interaction.guild.id})"
  try:
    cursor.execute(query)
    cursor.execute("commit")
  except mysql.connector.errors.IntegrityError:
    await interaction.followup.send("User is already being stalked.")
    return
  con.close()
  bot.stalk_list.append([interaction.user.id, user.id, interaction.guild.id])
  await interaction.followup.send("User is now being stalked. You creepy weirdo.")
    
@bot.tree.context_menu(name = "Stop Stalking")
async def untrack_user(interaction:discord.Interaction, user:discord.User):
  await interaction.response.defer(ephemeral = True)
  bot.stalk_list.remove([interaction.user.id, user.id, interaction.guild.id])
  con = mysql.connector.connect(user = USER, password = PASSWORD, 
                               host = HOST, database = DATABASE)
  cursor = con.cursor()
  query = f"delete from stalker_table where unique_id = \"{interaction.user.id}/{user.id}/{interaction.guild.id}\""
  cursor.execute(query)
  cursor.execute("commit")
  con.close()
  await interaction.followup.send("User is no longer being stalked. Good, you pervert.")

#Saves messages to MySQL that can be retrieved at any time.
@bot.tree.context_menu(name = "Save This Message")
async def savemessage(interaction:discord.Interaction, message:discord.Message):
  await interaction.response.defer(ephemeral = True)
  con = mysql.connector.connect(user = USER, password = PASSWORD, 
                               host = HOST, database = DATABASE)
  cursor = con.cursor()
  cursor.execute(f"insert into saved_messages values ({message.id}, \"{message.author.display_name}\", \"{message.content}\", {message.guild.id}, {message.author.id}, {interaction.user.id})")
  cursor.execute("commit")
  cursor.close()
  await interaction.followup.send("Message has been saved. Type /saved_messages to see your list of saved messages.")


##-------------------------------------------------------------- Slash Commands ----------------------------------------------------------------------------------------

@bot.tree.command(name = "create_poll", description = "Creates a poll for members of your server to vote on!")
@app_commands.describe(title = "The title of your poll.")
@app_commands.describe(option_one = "The first option on your poll")
@app_commands.describe(option_two = "The second option on your poll")
@app_commands.describe(option_three = "The third (optional) option of your poll.")
@app_commands.describe(group_mention = "Allows you to optionally mention either @here or @everyone")
@app_commands.choices(group_mention = [discord.app_commands.Choice(name = "@everyone", value = "@everyone"), discord.app_commands.Choice(name = "@here", value = "@here")])
async def poll(interaction:discord.Interaction, title:str, option_one:str, option_two:str, option_three:str = "",group_mention:discord.app_commands.Choice[str] = ""):
  if option_three.__eq__(""):
    view = twoPollButtons(title, option_one, option_two, interaction.user)
  else:
    view = threePollButtons(title, option_one, option_two, option_three, interaction.user)
  await interaction.response.send_message(group_mention, embed = view.embed, view = view)

@bot.tree.command(name = "create_mod_channel", description = "Creates a channel that is only visible to all ranks at or above the bot, for user/message reports.")
@app_commands.checks.has_permissions(administrator = True)
@app_commands.describe(name = "Name of your channel.")
async def mod_channel(interaction:discord.Interaction, name:str = "Moderator-Channel"):
  await interaction.response.defer(ephemeral = True)
  if not check(interaction.guild_id):
    overwrites = { ##Sets it so non admin roles cannot see the post upon creation.
      interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
      interaction.guild.me: discord.PermissionOverwrite(read_messages=True)
    }
    channel = await interaction.guild.create_text_channel(name, overwrites = overwrites)
    con = mysql.connector.connect(user = USER, password = PASSWORD, 
                               host = HOST, database = DATABASE)
    cursor = con.cursor()
    cursor.execute(f"insert into mod_channels values ({channel.guild.id}, {channel.id})")
    cursor.execute("commit")
    bot.mod_channels.append([channel.guild.id, channel.id])
    await interaction.followup.send("Channel has been created.")
  else:
    await interaction.followup.send("A moderation channel already exists in this server. Please delete your existing channel to make a new one.")

@bot.tree.command(name = "report_user", description = "Use this to report someone if you feel like you need a moderator to help.")
@app_commands.describe(user = "User you'd like to report.")
@app_commands.describe(reason = "Reason you're reporting this user.")
@app_commands.describe(anonymous = "Optional: Whether you'd like to make the report anonymous.")
async def report_user(interaction:discord.Interaction, user:discord.User, reason:str, anonymous:bool = False):
  def search():
    for i in bot.mod_channels:
      if i[0] == interaction.guild_id:
        return i[1]
    return None
  channel = bot.get_channel(search())
  if channel != None:
    tz = timezone('EST')
    if not anonymous:
      await channel.send(f"{interaction.user.display_name} reported {user.mention} at {str(datetime.now(tz))[:16]}. Reason: \"{reason}\"")
    else:
      await channel.send(f"An anonymous user reported {user.mention} at {str(datetime.now(tz))[:16]}. Reason: \"{reason}\"")
    await interaction.response.send_message(f"You have successfully reported {user.display_name}'s message.", ephemeral = True)
  else:
    await interaction.response.send_message("There is not a moderator channel set up in your server. Contact an admin to use /create_mod_channel to report messages.", ephemeral = True)
    
#Displays the messages saved from MySQL, or shows an error if there are no saved messages.
@bot.tree.command(name = "saved_messages", description = "Displays your list of saved messages.")
async def saved_messages(interaction:discord.Interaction):
  await interaction.response.defer()
  con = con = mysql.connector.connect(user = USER, password = PASSWORD, 
                               host = HOST, database = DATABASE)
  cursor = con.cursor()
  cursor.execute(f"select * from saved_messages where guild_id = {interaction.guild_id}")
  view = savedMessagesButtons(cursor, "**Saved Messages**")
  if len(view.embed_list) > 0:
    await interaction.followup.send(embed = view.embed_list[0], view = view)
  else:
    await interaction.followup.send(embed = discord.Embed(title = "Error: Empty List", description = "Looks like your server has no saved messages.\nTo save a message, right click any message --> Apps --> Save This Message"))
  con.close()

@bot.tree.command(name = "delete_saved_messages", description = "Deletes messages you've saved.")
async def delete_my_saved(interaction:discord.Interaction):
  await interaction.response.defer(ephemeral = True)
  con = mysql.connector.connect(user = USER, password = PASSWORD, 
                               host = HOST, database = DATABASE)
  cursor = con.cursor()
  cursor.execute(f"delete from saved_messages where guild_id = {interaction.guild_id} and saving_user_id = {interaction.user.id}")
  cursor.execute("commit")
  con.close()
  await interaction.followup.send("Messages have been deleted.")

@bot.tree.command(name = "help", description = "Some helpful advice if you're having trouble setting up your server.")
async def help_command(interaction:discord.Interaction):
  view = helpButtons()
  await view.initialize(interaction.channel)
  await interaction.response.send_message(f"{interaction.user.mention}", ephemeral = True)
        
    
@bot.tree.command(name = "remove_all_roles", description = "Removes all roles added using /add_role.")
@app_commands.checks.has_permissions(administrator = True)
async def remove_all(interaction:discord.Interaction):
  await interaction.response.defer(ephemeral = True)
  con = mysql.connector.connect(user = USER, password = PASSWORD, 
                                host = HOST, database = DATABASE)
  cursor = con.cursor()
  cursor.execute(f"select * from guild_roles where guild_id = {interaction.guild_id}")
  for x in cursor:
    role = discord.utils.get(interaction.guild.roles, name = x[1])
    await role.delete()
  cursor.execute(f"delete from guild_roles where guild_id = {interaction.guild_id}")
  cursor.execute("commit")
  await update_post(interaction.guild_id)
  await interaction.followup.send(f"Roles have been deleted.")

#Sets up all the mandatory channels for using the bot. This includes a role channel, bot channel, and all gender/DM roles to allow the buttons to work.
#Optional Boolean to set up a few game roles to start with.
@bot.tree.command(name = "server_setup", description = "Use this to set up basic server roles, a reaction channel, and a bot channel.")
@app_commands.describe(with_roles = "(True/False) Whether or not you'd like basic game roles added on setup (pronoun roles and DM roles are added either way).")
@app_commands.checks.has_permissions(manage_roles = True, manage_channels = True)
async def setup(interaction:discord.Interaction, with_roles:bool = True):
  await interaction.response.defer(ephemeral = True)
  necessary_roles = ["He/Him", "She/Her", "They/Them", "Other (ask)", "DMs Open", "Ask to DM", "DMs Closed"]
  for x in necessary_roles:
    role = discord.utils.get(interaction.guild.roles, name = x)
    if role == None:
      await interaction.guild.create_role(name = x)
  if with_roles:
    game_roles = [["Overwatch", "😤"], ["Phasmophobia", "👻"], ["Minecraft", "⛏️"], ["Valorant", "🔫"], ["League of Legends", "😡"]]
    for x in game_roles:
      await addRole(interaction.guild, x[0], x[1])
  role_channel = await interaction.guild.create_text_channel("react-for-roles")
  await role_channel.set_permissions(interaction.guild.default_role, send_messages = False)
  view = pronounButtons()
  await role_channel.send("**Pronoun Roles**", view = view)
  roles = roles2()    
  roles.channel = role_channel
  roles.guild = interaction.guild
  await roles.initialize()
  bot_channel = await interaction.guild.create_text_channel("bot-channel")
  con = mysql.connector.connect(user = USER, password = PASSWORD, 
                                host = HOST, database = DATABASE)
  cursor = con.cursor()
  query = f"insert into bot_channels values (\"{interaction.guild.id}\", \"{bot_channel.id}\")"
  try:
    cursor.execute(query)
    cursor.execute("commit")  
  except mysql.connector.errors.IntegrityError:
    pass
  await interaction.followup.send("Server setup is complete.")
    
#Generates an embed of a random Overwatch hero from overwatch.py.
#Optional parameters specify which role they'd like to receive a hero for.
@bot.tree.command(name = "random_hero", description = "Gives you a random Overwatch hero. Can specify what role.") 
@app_commands.describe(role = "What role you'd like a random hero for.")
@app_commands.choices(role = [discord.app_commands.Choice(name = "Tank", value = "tank"), discord.app_commands.Choice(name = "Damage", value = "damage"), discord.app_commands.Choice(name = "Support", value = "support")])
async def hero(interaction:discord.Interaction, role:discord.app_commands.Choice[str] = ""):
  if role.__eq__(""):
    hero = overwatch.getRandomHero()
  else:
    hero = overwatch.getRandomHero(role)
  if hero == None:
    await interaction.response.send_message("Invalid argument, please pick tank, damage, or support.")
  elif not hero == None:
    await interaction.response.send_message(embed = hero)      

#Displays embed of server commands. Fairly obsolete due to how slash commands work as a concept.
@bot.tree.command(name = "commands", description = "Displays a list of this bot's commands.")
async def command(interaction:discord.Interaction):
  view = commandButtons()
  await interaction.response.send_message(f"{interaction.user.mention}", embed = view.embed_list[0], view = view)

#Displays a leaderboard showing a ranking of members in the guild, according to how active they are in the guild.
@bot.tree.command(name = "leaderboard", description = "Displays the leaderboard for this server.")
async def leaderboard(interaction:discord.Interaction):
  con = mysql.connector.connect(user = USER, password = PASSWORD, 
                             host = HOST, database = DATABASE) 
  query = (f"select * from userinfo where guild_id = {interaction.guild_id} order by points desc")
  cursor = con.cursor()
  cursor.execute(query)
  view = Buttons(cursor, "**Server Leaderboard**")
  con.close()
  await interaction.response.send_message(f"{interaction.user.mention}", embed = view.embed_list[0], view = view)

#Sets the current channel as the channel to receive bot messages in. 
@bot.tree.command(name = "set_bot_channel", description = "Sets this channel for level up messages.")
@app_commands.checks.has_permissions(manage_channels = True)
async def bot_channel(interaction:discord.Interaction):
  con = mysql.connector.connect(user = USER, password = PASSWORD, 
                                host = HOST, database = DATABASE)
  cursor = con.cursor()
  try:
    query = f"insert into bot_channels values (\"{interaction.guild_id}\", \"{interaction.channel_id}\")"
    cursor.execute(query)
    cursor.execute("commit")
    await interaction.response.send_message("Channel has been made a bot channel!", ephemeral = True)
  except mysql.connector.errors.IntegrityError:
    await interaction.response.send_message("Channel is already a bot channel.", ephemeral = True)
  con.close()
  

#Generates a random embed of a middle finger. 
#Parameters include the user you'd like to mention (non-optional) and an additional message to go with it (optional)
@bot.tree.context_menu(name = "Flip off")
async def flip_off(interaction:discord.Interaction, user:discord.User):
  links = ["https://cdn.discordapp.com/attachments/1064811650298949642/1065682184033280051/Z.png", "https://cdn.discordapp.com/attachments/1064811650298949642/1065682244997501030/images.png", "https://cdn.discordapp.com/attachments/1064811650298949642/1065682456633671710/2Q.png", "https://cdn.discordapp.com/attachments/1064811650298949642/1065682604931694592/images.png", "https://cdn.discordapp.com/attachments/1064811650298949642/1065682701346164796/images.png", "https://cdn.discordapp.com/attachments/1064811650298949642/1065682815192145961/images.png", "https://cdn.discordapp.com/attachments/1064811650298949642/1065721204104769546/images.png", "https://cdn.discordapp.com/attachments/1064712978336841778/1065721748391202916/images.png", "https://cdn.discordapp.com/attachments/1064712978336841778/1065721797556834304/images.png", "https://cdn.discordapp.com/attachments/1064712978336841778/1065721845413838848/images.png", "https://cdn.discordapp.com/attachments/1064712978336841778/1065722323417710613/Z.png", "https://cdn.discordapp.com/attachments/1064811650298949642/1065721204104769546/images.png"]
  embed = discord.Embed()
  embed.set_image(url = links[random.randint(0, len(links) -1)])
  await interaction.response.send_message(f"{user.mention}", embed = embed)

#Adds a role to the server. Using this command to create a role will add it to the role post.
#If the role already exists, it adds the role to the database without creating a new role in the server.
#Parameters: The name of the role you're making, the emoji you'd like to associate with that role.
@bot.tree.command(name = "add_role", description = "Adds a role to this server.")
@app_commands.checks.has_permissions(manage_roles = True)
@app_commands.describe(role = "Role to add")
@app_commands.describe(emote = "Emote for reaction post")
async def add_role(interaction:discord.Interaction, role:str, emote:str):
  await interaction.response.defer(ephemeral = True)
  roleTest = discord.utils.get(interaction.guild.roles, name = role)
  query = f"insert into guild_roles values (\"{interaction.guild_id}/{role}\",\"{role}\",\"{interaction.guild_id}\",\"{emote}\")"
  con = mysql.connector.connect(user = USER, password = PASSWORD,
                                host = HOST, database = DATABASE)
  cursor = con.cursor()
  try:
    cursor.execute(query)
    cursor.execute("commit")
    if roleTest == None:
      await interaction.guild.create_role(name = role)
    await update_post(interaction.guild_id)
    await interaction.followup.send(f"{role} has been added as a role!")
  except mysql.connector.errors.IntegrityError:
    await interaction.followup.send(f"{role} already exists.")
  con.close()

#Toggles the server notifications for users leveling up. If this is disabled, it'll override personal settings to have the notification unmutes.
#Enabling this will not override a User's personal settings (see /mute and /unmute)
@bot.tree.command(name = "toggle_notifications", description = "Enables/disables the bot to notify and mention users on this server. Automatically disabled.")
@app_commands.checks.has_permissions(manage_channels = True)
async def enable_levels(interaction:discord.Interaction):
  await interaction.response.defer()
  con = mysql.connector.connect(user = USER, password = PASSWORD,
                                host = HOST, database = DATABASE)
  cursor = con.cursor()
  try:
    cursor.execute(f"insert into level_guilds values({interaction.guild_id})")
    cursor.execute("commit")
    bot.level_list.append(interaction.guild_id)
    await interaction.followup.send("Level messages are now enabled.")
  except mysql.connector.errors.IntegrityError:
    cursor.execute(f"delete from level_guilds where guild_id = ({interaction.guild_id})")
    cursor.execute("commit")
    bot.level_list.remove(interaction.guild_id)
    await interaction.followup.send("Level messages are now disabled.")
    
@bot.tree.command(name = "remove_role", description = "Removes a role from the server that was added using /add_role.")
@app_commands.checks.has_permissions(manage_roles = True)
@app_commands.describe(role = "Name of the role being deleted.")
async def remove_role(interaction:discord.Interaction, role:discord.Role):
  await interaction.response.defer(ephemeral = True)
  query = f"delete from guild_roles where unique_id = \"{interaction.guild_id}/{role}\""
  con = mysql.connector.connect(user = USER, password = PASSWORD, 
                               host = HOST, database = DATABASE)
  cursor = con.cursor()
  cursor.execute(query)
  cursor.execute("commit")
  await role.delete()
  await update_post(interaction.guild_id)
  await interaction.followup.send(f"{role.name} has been removed!")
  con.close()
    
@bot.tree.command(name = "clear_punishment_list", description = "Clears the list of punishments.")
@app_commands.checks.has_permissions(manage_channels = True)
async def clear_punishments(interaction:discord.Interaction):
  con = mysql.connector.connect(user = USER, password = PASSWORD, 
                               host = HOST, database = DATABASE)
  cursor = con.cursor()
  cursor.execute(f"delete from punishment_table where guild_id = {interaction.guild_id}")
  cursor.execute("commit")
  con.close()
  await interaction.response.send_message("Your list has been cleared!")
    
@bot.tree.command(name = "post_roles", description = "Creates a post for users to get roles. Please only make one per server.")
@commands.has_permissions(manage_channels = True, manage_roles = True)
async def post_roles(interaction:discord.Interaction):
  await interaction.response.defer(ephemeral = True)
  roles = roles2()    
  roles.channel = interaction.channel
  roles.guild = interaction.guild
  view = pronounButtons()
  await roles.channel.send("**Pronoun Roles**", view = view)
  await roles.initialize()
  await interaction.followup.send(f'{interaction.user.mention}')

@bot.tree.command(name = "mute", description = "Prevents the bot from notifying you when you level up.")
async def mute(interaction:discord.Interaction):
  con = mysql.connector.connect(user = USER, password = PASSWORD, 
                             host = HOST, database = DATABASE) 
  cursor = con.cursor()
  query = f"update userinfo set notification = false where unique_id = \"{interaction.user.id}/{interaction.guild_id}\""
  cursor.execute(query)
  cursor.execute("commit")
  con.close()
  await interaction.response.send_message("Bot has been muted.")

@bot.tree.command(name = "unmute", description = "Allows the bot to notify you upon leveling up.")
async def unmute(interaction:discord.Interaction):
  con = mysql.connector.connect(user = USER, password = PASSWORD, 
                                host = HOST, database = DATABASE)
  cursor = con.cursor()
  query = f"update userinfo set notification = true where unique_id = \"{interaction.user.id}/{interaction.guild_id}\""
  cursor.execute(query)
  cursor.execute("commit")
  con.close()
  await interaction.response.send_message("Bot has been unmuted.")
 
@bot.tree.command(name = "punishment_list", description = "Displays the list of punishments.")
async def punishments(interaction:discord.Interaction):
  con = mysql.connector.connect(user = USER, password = PASSWORD, 
                               host = HOST, database = DATABASE)
  cursor = con.cursor()
  cursor.execute(f"select * from punishment_table where guild_id = {interaction.guild_id}")
  view = punishment_buttons(cursor, "**Punishments**")
  await interaction.response.send_message(f"{interaction.user.mention}", embed = view.embed_list[0], view = view)
  
@bot.tree.command(name = "add_punishment", description = "Used to add a punishment to the server's punishment list.")
@app_commands.describe(punishment = "The punishment you want to add.")
async def add_punishment(interaction:discord.Interaction, punishment:str):
  con = mysql.connector.connect(user = USER, password = PASSWORD,
                               host = HOST, database = DATABASE)
  cursor = con.cursor()
  query = f"insert into punishment_table values (\"{punishment}\", \"{interaction.guild_id}\")"
  cursor.execute(query)
  cursor.execute("commit")
  await interaction.response.send_message("Punishment has been added.")
    
@bot.tree.command(name = "get_random_punishment", description = "Gets a random punishment from your server's list of punishments.")
@app_commands.describe(mention = "User you'd like to receive the punishment")
async def random_punishment(interaction:discord.Interaction, mention:discord.User = None):
  await interaction.response.defer()
  con = mysql.connector.connect(user = USER, password = PASSWORD, 
                               host = HOST, database = DATABASE)
  cursor = con.cursor()
  cursor.execute(f"select * from punishment_table where guild_id = {interaction.guild_id}")
  list = []
  for i in cursor:
    list.append(i)
  if len(list) != 0:
    if mention.__eq__(None):
      await interaction.followup.send(list[random.randint(0, len(list) - 1)][0])
    else:
      await interaction.followup.send(f"{mention.mention} got: {list[random.randint(0, len(list) - 1)][0]}")
  else:
    await interaction.followup.send("Your list is empty. Try adding some punishments using /add_punishment.")
 
@bot.tree.command(name = "random_agent", description = "Gives you a random agent from Valorant. Can specify the role you want.")
@app_commands.describe(role = "What role you'd like a random agent from.")
@app_commands.choices(role = [discord.app_commands.Choice(name = "Controller", value = "controller"), discord.app_commands.Choice(name = "Duelist", value = "duelist"), discord.app_commands.Choice(name = "Initiator", value = "initiator"), discord.app_commands.Choice(name = "Sentinel", value = "sentinel")])
async def agent(interaction:discord.Interaction, role:discord.app_commands.Choice[str] = ""):
  if role.__eq__(""):
    await interaction.response.send_message(f'{interaction.user.mention} your agent is {valorant.getRandomAgent()}')
    return
  agent = valorant.getRandomAgent(role = role)
  await interaction.response.send_message(f'{interaction.user.mention} your agent is {agent}.')

@bot.tree.command(name = "roll", description = "Roll any number of dice you'd like.")
@app_commands.describe(dice = "The number of dice you'd like to roll.")
@app_commands.describe(sides = "The number of sides on each die.")
async def roll(interaction:discord.Interaction, dice:int, sides:int): 
  stri = ' '
  for x in range(dice):
    stri += f'{x + 1} - {random.randint(1, sides)}'
  await interaction.response.send_message(f'{stri}')

@bot.tree.command(name = "random_map", description = "Generates a random map for Phasmophobia.")
@app_commands.describe(size = "Size of the map you want. Type \"not\" before the size to specify what not to get.")
@app_commands.choices(size = [discord.app_commands.Choice(name = "Small", value = "small"), discord.app_commands.Choice(name = "Medium", value = "medium"), discord.app_commands.Choice(name = "Large", value = "large"), discord.app_commands.Choice(name = "Not Small", value = "not small"), discord.app_commands.Choice(name = "Not Medium", value = "not medum"), discord.app_commands.Choice(name = "Not Large", value = "not large")])
async def map(interaction:discord.Interaction, size:discord.app_commands.Choice[str] =""):
  if size.__eq__(""):
    await interaction.response.send_message(f'{interaction.user.mention} you got', embed = phasmo.getEmbed())
  else:
    await interaction.response.send_message(f'{interaction.user.mention} you got', embed = phasmo.getEmbed(size))
    return
  await interaction.response.send_message(f'{interaction.user.mention} that is not a valid argument, a valid argument is small, medium, and large.') 
    
@bot.tree.command(name = "role_invite", description = "Creates a button for users to add a specific role, you can add an optional mention.")
@app_commands.describe(role = "The role you'd like to make the invite for.")
@app_commands.describe(group = "The group you would like to mention.")
@app_commands.choices(group = [discord.app_commands.Choice(name = "@everyone", value = "@everyone"), discord.app_commands.Choice(name = "@here", value = "@here")])
@app_commands.describe(individual = "The specifc user you'd like to mention.")
async def invite(interaction:discord.Interaction, role:discord.Role, group:discord.app_commands.Choice[str] = "", individual:discord.User = None):
  view = roleInviteButton(role)
  if not group.__eq__("") and individual != None:
    await interaction.response.send_message(f"{group.value}\n{individual.mention}\nYou have been invited to grab the **{role.name}** role.", view = view)
  elif not group.__eq__(""):
    await interaction.response.send_message(f"{group.value}\nYou have been invited to grab the **{role.name}** role.", view = view)
  elif individual != None:
    await interaction.response.send_message(f"{individual.mention}\nYou have been invited to grab the **{role.name}** role.", view = view)
  else:
    await interaction.response.send_message(f"You have been invited to grab the **{role.name}** role.", view = view)
    
@bot.tree.command(name = "challenge", description = "Challenge a friend to a game of rock paper scissors!")
@app_commands.describe(user = "A mentioned user's tag")
async def challenge(interaction:discord.Interaction, user:discord.User):
  member = user
  unique_id = ""
  p1_id = ""
  p2_id = ""
  p1_weapon = ""
  p2_weapon = ""
    
  view = Menu()
  view.p1_id = interaction.user.id
  view.p2_id = user.id
  await interaction.response.send_message(f"{interaction.user.mention} has challenged {user.mention}!\n**Please choose your weapon**", view = view)
  while not view.p1_status or not view.p2_status: 
    msg = await bot.wait_for("interaction")
  
  if (interaction.user.id > member.id):
    unique_id = f"{interaction.user.id}/{member.id}"
    p1_id = interaction.user.id
    p2_id = member.id
    p1_weapon = view.p1_choice
    p2_weapon = view.p2_choice
  else:
    unique_id = f"{member.id}/{interaction.user.id}"
    p1_id = member.id
    p2_id = interaction.user.id
    p1_weapon = view.p2_choice
    p2_weapon = view.p1_choice
  
  con = mysql.connector.connect(user = USER, password = PASSWORD, 
                             host = HOST, database = DATABASE) 
  cursor = con.cursor()
  cursor.execute(f"select * from rpsrecord WHERE player_combined_id = \"{unique_id}\"")
  time = datetime.now()
  list = []
  query = ""
  for points in cursor:
    list.append(points)
  if (len(list) == 0):   
    if p2_weapon.__eq__(p1_weapon):
      query = f"insert into rpsrecord values (\"{unique_id}\",\"{p1_id}\", \"{p2_id}\",\"{bot.get_user(p1_id).display_name}\",\"{bot.get_user(p2_id).display_name}\", 0, 0, 1, \"{str(time)[2:-7]}\", \"{interaction.guild_id}\")"
      cursor.execute(query)
      cursor.execute("commit")
      await interaction.channel.send(f"{bot.get_user(p1_id).mention} used {p1_weapon} and {bot.get_user(p2_id).mention} used {p2_weapon}.\nIt's a tie!\nCurrent record: {bot.get_user(p1_id).display_name} - 0, {bot.get_user(p2_id).display_name} - 0, Ties - 1")
    elif ((p2_weapon.__eq__('paper') and p1_weapon.__eq__('rock')) or (p2_weapon.__eq__('rock') and p1_weapon.__eq__('scissors')) or ((p2_weapon.__eq__('scissors')) and (p1_weapon.__eq__('paper')))):
      query = f"insert into rpsrecord values (\"{unique_id}\",\"{p1_id}\", \"{p2_id}\",\"{bot.get_user(p1_id).display_name}\",\"{bot.get_user(p2_id).display_name}\", 0, 1, 0, \"{str(time)[2:-7]}\", \"{interaction.guild_id}\")"
      cursor.execute(query)
      cursor.execute("commit")
      await interaction.channel.send(f"{bot.get_user(p1_id).mention} used {p1_weapon} and {bot.get_user(p2_id).mention} used {p2_weapon}.\n{bot.get_user(p2_id).display_name} wins!\nCurrent record: {bot.get_user(p1_id).display_name} - 0, {bot.get_user(p2_id).display_name} - 1, Ties - 0")
    elif ((p1_weapon.__eq__('paper') and p2_weapon.__eq__('rock')) or (p1_weapon.__eq__('rock') and p2_weapon.__eq__('scissors')) or ((p1_weapon.__eq__('scissors')) and (p2_weapon.__eq__('paper')))):
      query = f"insert into rpsrecord values (\"{unique_id}\",\"{p1_id}\", \"{p2_id}\",\"{bot.get_user(p1_id).display_name}\",\"{bot.get_user(p2_id).display_name}\", 1, 0, 0, \"{str(time)[2:-7]}\", \"{interaction.guild_id}\")"
      cursor.execute(query)
      cursor.execute("commit")
      await interaction.channel.send(f"{bot.get_user(p1_id).mention} used {p1_weapon} and {bot.get_user(p2_id).mention} used {p2_weapon}.\n{bot.get_user(p1_id).display_name} wins!\nCurrent record: {bot.get_user(p1_id).display_name} - 1, {bot.get_user(p2_id).display_name} - 0, Ties - 0")
  else:
    newlist = list[0]
    list.pop(0)
    if p2_weapon.__eq__(p1_weapon):
      query = f"update rpsrecord set player_1_display_name = \"{bot.get_user(p1_id).display_name}\", player_2_display_name = \"{bot.get_user(p2_id).display_name}\", last_time_played = \"{str(time)[2:-7]}\", ties = {newlist[7] + 1} where player_combined_id = \"{unique_id}\""
      cursor.execute(query)
      cursor.execute("commit")
      await interaction.channel.send(f"{bot.get_user(p1_id).mention} used {p1_weapon} and {bot.get_user(p2_id).mention} used {p2_weapon}.\nIt's a tie!\nCurrent record: {bot.get_user(p1_id).display_name} - {newlist[5]}, {bot.get_user(p2_id).display_name} - {newlist[6]}, Ties - {newlist[7] + 1}")
    elif ((p2_weapon.__eq__('paper') and p1_weapon.__eq__('rock')) or (p2_weapon.__eq__('rock') and p1_weapon.__eq__('scissors')) or ((p2_weapon.__eq__('scissors')) and (p1_weapon.__eq__('paper')))):
      query = f"update rpsrecord set player_1_display_name = \"{bot.get_user(p1_id).display_name}\", player_2_display_name = \"{bot.get_user(p2_id).display_name}\", last_time_played = \"{str(time)[2:-7]}\", p2_points = {newlist[6] + 1} where player_combined_id = \"{unique_id}\""
      cursor.execute(query)
      cursor.execute("commit")
      await interaction.channel.send(f"{bot.get_user(p1_id).mention} used {p1_weapon} and {bot.get_user(p2_id).mention} used {p2_weapon}.\n{bot.get_user(p2_id).display_name} wins!\nCurrent record: {bot.get_user(p1_id).display_name} - {newlist[5]}, {bot.get_user(p2_id).display_name} - {newlist[6] + 1}, Ties - {newlist[7]}")
    elif ((p1_weapon.__eq__('paper') and p2_weapon.__eq__('rock')) or (p1_weapon.__eq__('rock') and p2_weapon.__eq__('scissors')) or ((p1_weapon.__eq__('scissors')) and (p2_weapon.__eq__('paper')))):
      query = f"update rpsrecord set player_1_display_name = \"{bot.get_user(p1_id).display_name}\", player_2_display_name = \"{bot.get_user(p2_id).display_name}\", last_time_played = \"{str(time)[2:-7]}\", p1_points = {newlist[5] + 1} where player_combined_id = \"{unique_id}\""
      cursor.execute(query)
      cursor.execute("commit")
      await interaction.channel.send(f"{bot.get_user(p1_id).mention} used {p1_weapon} and {bot.get_user(p2_id).mention} used {p2_weapon}.\n{bot.get_user(p1_id).display_name} wins!\nCurrent record: {bot.get_user(p1_id).display_name} - {newlist[5] + 1}, {bot.get_user(p2_id).display_name} - {newlist[6]}, Ties - {newlist[7]}")
  con.close()

@bot.tree.command(name = "hangman", description = "Play Hangman.")
@app_commands.describe(content = "The word(s) or phrase you'd like others to guess.")
@app_commands.describe(guesses = "The amount of guesses allowed for your word.")
async def hangman(interaction:discord.Interaction, content:str, guesses:int = 6):
  view = hangman_game.hangmanButtons(content, interaction.channel, guesses)
  await interaction.response.send_message(f'{view.string}\n\nStrikes Left: {view.attempts}\nGuessed letters:', view = view)
##---------------------------------------------------------------------Functions-------------------------------------------------------------------------------------

def factorial(num):
  if (num <= 0):
    return 0
  if (num == 1):
    return 1
  else:
    return num + factorial(num - 1)

def check(id): ##Used to check for a matching guild id in mod_channels list
  for i in bot.mod_channels:
    if i[1].__eq__(id) or i[0].__eq__(id):
      return True
  return False

def addSeconds(input:datetime, seconds:int):
  if (seconds < 0 or seconds > 60):
    raise ValueError("Not a valid input.")
  daysInMonths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
  second = input.second
  if (second + seconds) > 60:
    if (input.minute + 1 == 60):
      if (input.hour + 1 == 24):
        if (input.day + 1 > daysInMonths[input.month - 1]):
          if (input.month + 1 > 12):
            check = input.replace(year = input.year + 1, month = 1, day = 1, hour = 0, minute = 0, second = (second + seconds)%60)
          else:
            check = input.replace(month = input.month + 1, day = 1, hour = 0, minute = 0, second = (second + seconds)%60)
        else:
          check = input.replace(day = input.day + 1, hour = 0, minute = 0, second = (second + seconds)%60)
      else: 
        check = input.replace(hour = input.hour + 1, minute = 0, second = (second + seconds)%60)
    else:
      check = input.replace(minute = input.minute + 1, second = (second + seconds)%60)
  else:
    check = input.replace(second=second + 5)
  return check

def addDays(input:datetime, days:int):
  daysInMonths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
  if (days < 0 or days > daysInMonths[input.month-1]):
    raise ValueError("Not a valid input.")
  day = input.day
  if (day + days) > daysInMonth[input.month - 1]:
    if (input.month + 1 > 12):
      newdatetime = input.replace(year = input.year + 1, month = 1, day = (input.day + days)%daysInMonths[input.month - 1])
    else:
      newdatetime = input.replace(month = input.month + 1, day = (input.day + days)%daysInMonths[input.month - 1])
  else:
    newdatetime = input.replace(day = input.day + days)
  return newdatetime    

def toDateTime(input):
  return datetime.strptime(input, '%y-%m-%d %H:%M:%S')

async def update_post(guild_id):
  con = mysql.connector.connect(user = USER, password = PASSWORD,
                                host = HOST, database = DATABASE)
  cursor = con.cursor()
  query = f"select * from guild_roles where guild_id = \"{guild_id}\" order by name asc"
  cursor.execute(query)
  string = "**React here for roles**\n"
  emojis = []
  for i in cursor:
    string += f"{i[1]}: {i[3]}\n"
    emojis.append(i[3])
  cursor.execute(f"select * from reaction_messages where guild_id = {guild_id}")
  list = []
  for i in cursor:
    list.append(i)
  for i in list:
    channel = bot.get_channel(int(i[2]))
    message = await channel.fetch_message(int(i[0]))
    await message.edit(content = string)
    for x in emojis:
      await message.add_reaction(x)
    for i in message.reactions:
      if i.emoji not in emojis:
        await message.clear_reaction(i.emoji)
  

async def addRole(guild, role, emote):
  roletest = discord.utils.get(guild.roles, name = role)
  query = f"insert into guild_roles values (\"{guild.id}/{role}\",\"{role}\",\"{guild.id}\",\"{emote}\")"
  con = mysql.connector.connect(user = USER, password = PASSWORD,
                                host = HOST, database = DATABASE)
  cursor = con.cursor()
  try:
    cursor.execute(query)
    cursor.execute("commit")
  except mysql.connector.errors.IntegrityError:
    con.close()
    return
  con.close()
  if roletest == None: ##Creates the role if it does not exist, otherwise it just adds the role to the database.
    await guild.create_role(name = role)

##------------------------------------------------------------------Bot Events-------------------------------------------------------------------------------

@bot.event
async def on_message(message):
  if message.author.id != bot.user.id and message.author.id != 1057542778604765225: ##Manages the level up database, adds points based on messages sent.
    con = mysql.connector.connect(user = USER, password = PASSWORD, 
                             host = HOST, database = DATABASE) 
    cursor = con.cursor()
    cursor.execute(f"select * from userinfo WHERE unique_id = \"{message.author.id}/{message.author.guild.id}\"")
    time = datetime.now()
    list = []
    for points in cursor:
      list.append(points)
    if (len(list) == 0):
      query = (f"insert into userinfo values (\"{message.author.id}/{message.author.guild.id}\", \"{str(time)[2:-7]}\", \"{message.author.display_name}\", \"{message.author.mention}\", 1, 1, {message.author.guild.id}, 1)")
      cursor.execute(query)
      cursor.execute("commit")
      cursor.execute(f"select * from bot_channels where guild_id = \"{message.guild.id}\"") 
      channel = ""
      list1 = []
      for x in cursor:
        list1.append(x)
      if len(list1) == 0:
        channel = message.channel
      else:
        channel = bot.get_channel(int(list1[0][1]))
      if message.guild.id in bot.level_list:
        await channel.send(f"{message.author.mention} Congratulations! You've reached level 1!")
    elif toDateTime(list[0][1]) <= datetime.now():
      point = list[0][4] + 1
      if (point) == (factorial(list[0][5]) * 2) + 2:
        query = (f"update userinfo set display_name = \"{message.author.display_name}\", time = \"{str(addSeconds(time, 20))[2:-7]}\", points = {point}, level = {list[0][5] + 1} where unique_id = \"{message.author.id}/{message.author.guild.id}\"")
        cursor.execute(query)
        cursor.execute("commit")
        cursor.execute(f"select * from bot_channels where guild_id = \"{message.guild.id}\"")
        channel = ""
        list1 = []
        for x in cursor:
          list1.append(x)
        if len(list1) == 0:
          channel = message.channel
        else:
          channel = bot.get_channel(int(list1[0][1]))
        if (list[0][7]) and not message.content.__eq__(".mute") and message.guild.id in bot.level_list:
          await channel.send(f"{message.author.mention} Congratulations! You've reached level {list[0][5] + 1}!")
      else:
        query = (f"update userinfo set display_name = \"{message.author.display_name}\", time = \"{str(addSeconds(time, 20))[2:-7]}\", points = {point} where unique_id = \"{message.author.id}/{message.author.guild.id}\"")
        cursor.execute(query)
        cursor.execute("commit")
  await bot.process_commands(message)

@bot.event
async def on_presence_update(before, after):
  if before.status == discord.Status.offline: ##Used for the Stalk command.
    if after.status == discord.Status.online:
      list = []
      for i in bot.stalk_list:
        if i[1] == before.id and i[2] == before.guild.id:
          list.append(i)
      for i in list:
        user = bot.get_user(i[0])
        await user.send(f"{before.display_name} is now online.")
#For me to see when an error occurs and when.        
@bot.event
async def on_command_error(ctx, error):
  print(f"{error} at {datetime.now()} in {ctx.channel}")


@bot.event
async def on_guild_join(guild):
    general = discord.utils.find(lambda x: x.name == 'general',  guild.text_channels) ##Sends a message to a general-chat channel when the bot joins a server
    if general and general.permissions_for(guild.me).send_messages:
        await general.send("Thank you for adding me to your server! To get started, type /server_setup. To enable level-up notifications, please type /toggle_level")    
        
@bot.event
async def on_member_join(member):
  if member.guild.id in bot.level_list:
    con = mysql.connector.connect(user = USER, password = PASSWORD,
                               host = HOST, database = DATABASE)
    cursor = con.cursor()
    cursor.execute(f"select * from bot_channels where guild_id = \"{member.guild.id}\"")
    channel = ""
    list1 = []
    for x in cursor:
      list1.append(x)
    channel = bot.get_channel(int(list1[0][1]))
    await channel.send(f"Welcome {member.mention}, make sure to grab some roles so people know you mean business :sunglasses:")    ##Sends a message to new members, should the server not be muted
    
@bot.event
async def on_guild_channel_delete(channel): 
  con = mysql.connector.connect(user = USER, password = PASSWORD, ##Clears database when a channel containing a reaction post, bot channel, or mod channel is deleted. Keeps database tidy-ish.
                               host = HOST, database = DATABASE)
  cursor = con.cursor()
  cursor.execute(f"select * from bot_channels where channel_id = {channel.id}")
  list = []
  for x in cursor:
    list.append(x)
  if (len(list) != 0):
    cursor.execute(f"delete from bot_channels where channel_id = {channel.id}")
    cursor.execute("commit")
  cursor.execute(f'select * from reaction_messages where channel_id = {channel.id}')
  list = []
  for x in cursor:
    list.append(x)
  if len(list) != 0:
    cursor.execute(f"delete from reaction_messages where channel_id = {channel.id}")
    cursor.execute("commit")
    bot.reaction_list.remove(channel.id)
  cursor.execute(f'select * from mod_channels where channel_id = {channel.id}')
  list = []
  for x in cursor:
    list.append(x)
  if len(list) != 0:
    cursor.execute(f"delete from mod_channels where channel_id = {channel.id}")
    cursor.execute("commit")
    for x in bot.mod_channels:
      if x[1].__eq__(channel.id):
        bot.mod_channels.remove(x)
  con.close()

@bot.event
async def on_raw_reaction_add(payload):
  if payload.message_id in bot.reaction_list and payload.member.id != bot.user.id: ##Adds roles when a reaction is added to a reaction post.
    con = mysql.connector.connect(user = USER, password = PASSWORD, 
                                  host = HOST, database = DATABASE)
    cursor = con.cursor()
    query = f"select * from guild_roles where guild_id = \"{payload.guild_id}\" and emoji = \"{payload.emoji.name}\""
    cursor.execute(query)
    guild = bot.get_guild(payload.guild_id)
    list = []
    for x in cursor:
      list.append(x)
    for i in list:
      if payload.emoji.name.__eq__(i[3]):
        role = discord.utils.get(guild.roles, name = i[1])
        await payload.member.add_roles(role)

    
@bot.event
async def on_raw_reaction_remove(payload):
  if payload.message_id in bot.reaction_list: ##Removes roles when a reaction is removed from a reaction post.
    con = mysql.connector.connect(user = USER, password = PASSWORD, 
                                  host = HOST, database = DATABASE)
    cursor = con.cursor()
    query = f"select * from guild_roles where guild_id = \"{payload.guild_id}\" and emoji = \"{payload.emoji.name}\""
    cursor.execute(query)
    guild = bot.get_guild(payload.guild_id)
    list = []
    for x in cursor:
      list.append(x)
    for i in list:
      if payload.emoji.name.__eq__(i[3]):
        role = discord.utils.get(guild.roles, name = i[1])
        await guild.get_member(payload.user_id).remove_roles(role)
        
@bot.event
async def on_raw_message_delete(payload):
  if payload.message_id in bot.reaction_list: ##Clears database and reaction_list when a reaction message is deleted to keep database tidy-ish.
    bot.reaction_list.remove(payload.message_id)
    con = mysql.connector.connect(user = USER, password = PASSWORD, 
                                  host = HOST, database = DATABASE)
    cursor = con.cursor()
    query = f"delete from reaction_messages where message_id = {payload.message_id}"
    cursor.execute(query)
    cursor.execute("commit")
    con.close()
    print("Message successfully removed.")
##------------------------------------------------------------------------Button Objects--------------------------------------------------------------------------------------------------------
class roleInviteButton(discord.ui.View):
  def __init__(self, role:discord.Role):
    super().__init__(timeout = None)
    self.role = role
  @discord.ui.button(label = "Take Role", style = discord.ButtonStyle.green)
  async def button(self, interaction:discord.Interaction, button:discord.Button):
    await interaction.user.add_roles(self.role)
    await interaction.response.defer()
class pronounButtons(discord.ui.View):
  def __init__(self):
    super().__init__(timeout = None)
  @discord.ui.button(label = "He/Him", style = discord.ButtonStyle.blurple, custom_id = "persistent_view:he")
  async def button1(self, interaction:discord.Interaction, button: discord.ui.Button): 
    role = discord.utils.get(interaction.guild.roles, name = "He/Him")
    if role in interaction.user.roles:
      await interaction.user.remove_roles(role)
      await interaction.response.defer()
    else:
      await interaction.user.add_roles(role)
      await interaction.response.defer()
  @discord.ui.button(label = "She/Her", style = discord.ButtonStyle.blurple, custom_id = "persistent_view:her")
  async def button2(self, interaction:discord.Interaction, button: discord.ui.Button): 
    role = discord.utils.get(interaction.guild.roles, name = "She/Her")
    if role in interaction.user.roles:
      await interaction.user.remove_roles(role)
      await interaction.response.defer()
    else:
      await interaction.user.add_roles(role)
      await interaction.response.defer()
  @discord.ui.button(label = "They/Them", style = discord.ButtonStyle.blurple, custom_id = "persistent_view:they")
  async def button3(self, interaction:discord.Interaction, button: discord.ui.Button): 
    role = discord.utils.get(interaction.guild.roles, name = "They/Them")
    if role in interaction.user.roles:
      await interaction.user.remove_roles(role)
      await interaction.response.defer()
    else:
      await interaction.user.add_roles(role)
      await interaction.response.defer()
  @discord.ui.button(label = "Other (ask)", style = discord.ButtonStyle.blurple, custom_id = "persistent_view:other")
  async def button4(self, interaction:discord.Interaction, button: discord.ui.Button): 
    role = discord.utils.get(interaction.guild.roles, name = "Other (ask)")
    if role in interaction.user.roles:
      await interaction.user.remove_roles(role)
      await interaction.response.defer()
    else:
      await interaction.user.add_roles(role)
      await interaction.response.defer()

class helpButtons(discord.ui.View):
  def __init__(self):
    super().__init__(timeout = None)
    self.channel = ""
    self.cursor = 0
    self.embed_list = []
  async def initialize(self, channel):
    instructions = "If you've got a new server, type /server_setup to get started. It'll add a role-channel with a role post, a bot-channel to funnel level up messages into (these messages are automatically disabled, type /toggle_levels), and optionally you can type \"True\" to include a few premade game roles. Use add_role to add more roles."
    instructions2 = "If your server isn't new and you already have a role-channel and a bot channel, you can set up your server manually. Using /post_roles will create a role post in whichever channel you use the command (Note: Only roles added using /add_role will show up on the roles post. You can add pre-existing roles to the list, as long as you type in the name of the role exactly in the command). Using /set_bot_channel, you can set the bot channel to whichever channel you used the command in."
    bugs_qa = "Q: \"My pronoun and/or DM buttons on the role post aren't working.\"\nA: Make sure they're named the exact same as the buttons are labelled. Currently there is no way to customize these buttons or their names.\n\nQ: \"There are no level up messages after setting up the bot channel\"\nA: Call the /toggle_levels command, that should enable it. If not, make sure you or whoever you're looking at hasn't used /mute."
    self.embed_list.append(discord.Embed(title = "New Server Help", description = instructions, colour = discord.Colour.blue()))
    self.embed_list.append(discord.Embed(title = "Existing Server Help", description = instructions2, colour = discord.Colour.blue()))
    self.embed_list.append(discord.Embed(title = "Issues Q&A", description = bugs_qa, colour = discord.Colour.blue()))
    self.channel = channel
    await channel.send(embed = self.embed_list[0], view = self)
  @discord.ui.button(label = "<--", style = discord.ButtonStyle.blurple, custom_id = "persistent_view:left_help")
  async def button1(self, interaction:discord.Interaction, button: discord.ui.Button): 
    if self.cursor == 0:
      await interaction.response.defer()
    else:
      self.cursor -= 1
      await interaction.response.edit_message(embed = self.embed_list[self.cursor])
  @discord.ui.button(label = "-->", style = discord.ButtonStyle.blurple, custom_id = "persistent_view:right_help")
  async def button2(self, interaction:discord.Interaction, button: discord.ui.Button):
    if self.cursor == len(self.embed_list) - 1:
      await interaction.response.defer()
    else:
      self.cursor += 1
      await interaction.response.edit_message(embed = self.embed_list[self.cursor])

class commandButtons(discord.ui.View):
  def __init__(self):
    super().__init__(timeout = None)
    self.cursor = 0
    helpEmbed = discord.Embed(title = "__Commands:__", colour = discord.Colour.blue())
    helpEmbed.add_field(name = '_Game Commands_', value = '\n- /hero (role): Selects random hero, of the role if there is one specified. (Overwatch)\n\n- /map (size): Selects a random map. Will select from a specified size if one is specified (Phasmophobia)\n\n- /agent (role): Selects random agent, of the specified role if there is one.\n\n- /roll: Rolls a specified number of #-sided dice.\n\n- /challenge (User Mention) Challenges the mentioned user to trial by combat'.format())
    helpEmbed.set_footer(text = '~~Maidenless Commands~~')
    helpEmbed2 = discord.Embed(title = "__Commands:__", colour = discord.Colour.blue())
    helpEmbed2.add_field(name = "_Leaderboard Commands_", value = "\n- /leaderboard: Displays the server leaderboard.\n\n- /mute: Stops the bot from notifying you on leveling up. \n\n- /unmute: Reverts the effects of the mute command.")
    helpEmbed2.set_footer(text = '~~Maidenless Commands~~')
    helpEmbed3 = discord.Embed(title = "__Commands:__", colour = discord.Colour.blue())
    helpEmbed3.add_field(name = "_Administrator Commands_", value = "\n- /post_roles: Creates a post for users to get roles from. Please only have one role post in a server at a time.\n\n- /add_role: Adds a role to the server.\n\n- /remove_role: Removes a role that was previously added with add_role (manually deleting the role won't work).\n\n- /remove_all_roles: Removes all roles added with /add_role.\n\n- /set_bot_channel: sets the current channel as the channel for level up notifications to funnel through.")
    helpEmbed3.set_footer(text = "~~Maidenless Commands~~")
    self.embed_list = [helpEmbed, helpEmbed2, helpEmbed3]
  @discord.ui.button(label = "<--", style = discord.ButtonStyle.blurple, custom_id = "persistent_view:left2")
  async def button1(self, interaction:discord.Interaction, button: discord.ui.Button): 
    if self.cursor == 0:
      await interaction.response.defer()
    else:
      self.cursor -= 1
      await interaction.response.edit_message(embed = self.embed_list[self.cursor])
  @discord.ui.button(label = "-->", style = discord.ButtonStyle.blurple, custom_id = "persistent_view:right2")
  async def button2(self, interaction:discord.Interaction, button: discord.ui.Button):
    if self.cursor == len(self.embed_list) - 1:
      await interaction.response.defer()
    else:
      self.cursor += 1
      await interaction.response.edit_message(embed = self.embed_list[self.cursor])
        
class punishment_buttons(discord.ui.View):
  def __init__(self, sqlcursor , title:str):
    super().__init__(timeout = None)
    self.embed_list = []
    self.sql = sqlcursor
    self.cursor = 0
    self.title = title
    self.initialize()
  def initialize(self):
    accumulator = 0
    string = ""
    for x in self.sql:
      string += f"{x[0]}\n"
      accumulator += 1
      if accumulator == 10:
        self.embed_list.append(discord.Embed(title = self.title,
                       description = string,
                       color = discord.Color.red()))
        accumulator = 1
        string = ""
    self.embed_list.append(discord.Embed(title = self.title,
                       description = string,
                       color = discord.Color.red()))
  @discord.ui.button(label = "<--", style = discord.ButtonStyle.blurple, custom_id = "persistent_view:left2")
  async def button1(self, interaction:discord.Interaction, button: discord.ui.Button): 
    if self.cursor == 0:
      await interaction.response.defer()
    else:
      self.cursor -= 1
      await interaction.response.edit_message(embed = self.embed_list[self.cursor])
  @discord.ui.button(label = "-->", style = discord.ButtonStyle.blurple, custom_id = "persistent_view:right2")
  async def button2(self, interaction:discord.Interaction, button: discord.ui.Button):
    if self.cursor == len(self.embed_list) - 1:
      await interaction.response.defer()
    else:
      self.cursor += 1
      await interaction.response.edit_message(embed = self.embed_list[self.cursor])
        
class savedMessagesButtons(discord.ui.View):
  def __init__(self, sqlcursor , title:str):
    super().__init__(timeout = None)
    self.embed_list = []
    self.sql = sqlcursor
    self.cursor = 0
    self.title = title
    self.initialize()
  def initialize(self):
    accumulator = 0
    string = ""
    for x in self.sql:
      stri = x[2].replace("\n", " ")
      string += x[1].ljust(20) + " - {}\n".format(stri)
      accumulator += 1
      if accumulator == 10:
        self.embed_list.append(discord.Embed(title = self.title,
                       description = string,
                       color = discord.Color.red()))
        accumulator = 1
        string = ""
    if not string .__eq__(""):
        self.embed_list.append(discord.Embed(title = self.title,
                       description = string,
                       color = discord.Color.red()))
  @discord.ui.button(label = "<--", style = discord.ButtonStyle.blurple, custom_id = "persistent_view:left3")
  async def button1(self, interaction:discord.Interaction, button: discord.ui.Button): 
    if self.cursor == 0:
      await interaction.response.defer()
    else:
      self.cursor -= 1
      await interaction.response.edit_message(embed = self.embed_list[self.cursor])
  @discord.ui.button(label = "-->", style = discord.ButtonStyle.blurple, custom_id = "persistent_view:right3")
  async def button2(self, interaction:discord.Interaction, button: discord.ui.Button):
    if self.cursor == len(self.embed_list) - 1:
      await interaction.response.defer()
    else:
      self.cursor += 1
      await interaction.response.edit_message(embed = self.embed_list[self.cursor])
        
class Buttons(discord.ui.View): #Currently only used for displaying the server leaderboard.
  def __init__(self, sqlcursor , title:str):
    super().__init__(timeout = None)
    self.embed_list = []
    self.sql = sqlcursor
    self.cursor = 0
    self.title = title
    self.initialize()
  def initialize(self):
    accumulator = 0
    string = ""
    for x in self.sql:
      string += f"{accumulator + 1}. {x[2]} - {x[5]}\n"
      accumulator += 1
      if accumulator % 10 == 0:
        self.embed_list.append(discord.Embed(title = self.title,
                       description = string,
                       color = discord.Color.red()))
        string = ""
    if not string .__eq__(""):
        self.embed_list.append(discord.Embed(title = self.title,
                       description = string,
                       color = discord.Color.red()))
  @discord.ui.button(label = "<--", style = discord.ButtonStyle.blurple, custom_id = "persistent_view:left3")
  async def button1(self, interaction:discord.Interaction, button: discord.ui.Button): 
    if self.cursor == 0:
      await interaction.response.defer()
    else:
      self.cursor -= 1
      await interaction.response.edit_message(embed = self.embed_list[self.cursor])
  @discord.ui.button(label = "-->", style = discord.ButtonStyle.blurple, custom_id = "persistent_view:right3")
  async def button2(self, interaction:discord.Interaction, button: discord.ui.Button):
    if self.cursor == len(self.embed_list) - 1:
      await interaction.response.defer()
    else:
      self.cursor += 1
      await interaction.response.edit_message(embed = self.embed_list[self.cursor])


class roles2(discord.ui.View): #There is no roles1
  def __init__(self):
    super().__init__(timeout = None)
    self.value = 0
    self.message_id_one = ""
    self.user = ""
    self.channel = ""
    self.guild = ""
  
  async def initialize(self):
    con = mysql.connector.connect(user = USER, password = PASSWORD,
                                host = HOST, database = DATABASE)
    cursor = con.cursor()
    query = f"select * from guild_roles where guild_id = \"{self.guild.id}\" order by name asc"
    cursor.execute(query)
    string = "**Gamer Roles**\n"
    emojis = []
    for i in cursor:
      string += f"{i[1]}: {i[3]}\n"
      emojis.append(i[3])
    message = await self.channel.send(string)
    for i in emojis:
      await message.add_reaction(i)
    if message.id not in bot.reaction_list:
      bot.reaction_list.append(message.id)
    query = f"insert into reaction_messages values ({message.id}, {message.guild.id}, {message.channel.id})"
    cursor.execute(query)
    cursor.execute("commit")
    con.close()
    await self.channel.send("**DM Roles**", view = self)
  @discord.ui.button(label = "DMs Open", style = discord.ButtonStyle.green , custom_id = "persistent_view:yes")
  async def button1(self, interaction:discord.Interaction, button: discord.ui.Button):
    role = discord.utils.get(interaction.guild.roles, name = "DMs Open")
    role2 = discord.utils.get(interaction.guild.roles, name = "Ask to DM")
    role3 = discord.utils.get(interaction.guild.roles, name = "DMs Closed")
    if role in interaction.user.roles:
      await interaction.user.remove_roles(role)
    elif role2 in interaction.user.roles:
      await interaction.user.remove_roles(role2)
      await interaction.user.add_roles(role)
    elif role3 in interaction.user.roles:
      await interaction.user.remove_roles(role3)
      await interaction.user.add_roles(role)
    else:
      await interaction.user.add_roles(role)
    await interaction.response.defer()
  @discord.ui.button(label = "Ask to DM", style = discord.ButtonStyle.blurple, custom_id= "persistent_view:maybe")
  async def button2(self, interaction:discord.Interaction, button: discord.ui.Button):
    role = discord.utils.get(interaction.guild.roles, name = "Ask to DM")
    role2 = discord.utils.get(interaction.guild.roles, name = "DMs Open")
    role3 = discord.utils.get(interaction.guild.roles, name = "DMs Closed")
    if role in interaction.user.roles:
      await interaction.user.remove_roles(role)
    elif role2 in interaction.user.roles:
      await interaction.user.remove_roles(role2)
      await interaction.user.add_roles(role)
    elif role3 in interaction.user.roles:
      await interaction.user.remove_roles(role3)
      await interaction.user.add_roles(role)
    else:
      await interaction.user.add_roles(role)
    await interaction.response.defer()
  @discord.ui.button(label = "DMs Closed", style = discord.ButtonStyle.red, custom_id="persistent_view:no")
  async def button3(self, interaction:discord.Interaction, button: discord.ui.Button):
    role = discord.utils.get(interaction.guild.roles, name = "DMs Closed")
    role2 = discord.utils.get(interaction.guild.roles, name = "Ask to DM")
    role3 = discord.utils.get(interaction.guild.roles, name = "DMs Open")
    if role in interaction.user.roles:
      await interaction.user.remove_roles(role)
    elif role2 in interaction.user.roles:
      await interaction.user.remove_roles(role2)
      await interaction.user.add_roles(role)
    elif role3 in interaction.user.roles:
      await interaction.user.remove_roles(role3)
      await interaction.user.add_roles(role)
    else:
      await interaction.user.add_roles(role)
    await interaction.response.defer()

### RPS Code

class Menu(discord.ui.View): ##Button Object for rock paper scissors
  def __init__(self):
    super().__init__(timeout = None)
    self.value = 0
    self.p1_id = ""
    self.p2_id = ""
    self.p1_status = False
    self.p2_status = False
    self.p1_choice = ""
    self.p2_choice = ""  
    
  @discord.ui.button(label = "Rock", style=discord.ButtonStyle.green, custom_id = "persistent_view:rock")
  async def menu1(self, interaction:discord.Interaction, button:discord.ui.Button):
    if interaction.user.id.__eq__(self.p1_id) and self.p1_status == False:
      self.p1_choice = "rock"
      self.p1_status = True  
    elif interaction.user.id.__eq__(self.p2_id) and self.p2_status == False:
      self.p2_choice = "rock"
      self.p2_status = True     
    await interaction.response.defer()
    
  @discord.ui.button(label = "Paper", style=discord.ButtonStyle.blurple, custom_id = "persistent_view:paper")
  async def menu2(self, interaction:discord.Interaction, button:discord.ui.Button):
    if interaction.user.id.__eq__(self.p1_id) and self.p1_status == False:
      self.p1_choice = "paper"
      self.p1_status = True
    elif interaction.user.id.__eq__(self.p2_id) and self.p2_status == False:
      self.p2_choice = "paper"
      self.p2_status = True
    await interaction.response.defer()
    
  @discord.ui.button(label = "Scissors", style=discord.ButtonStyle.red, custom_id = "persistent_view:scissors")
  async def menu3(self, interaction:discord.Interaction, button:discord.ui.Button):
    if interaction.user.id.__eq__(self.p1_id) and self.p1_status == False:
      self.p1_choice = "scissors"
      self.p1_status = True
    elif interaction.user.id.__eq__(self.p2_id) and self.p2_status == False:
      self.p2_choice = "scissors"
      self.p2_status = True
    await interaction.response.defer()


class twoPollButtons(discord.ui.View):
  def __init__(self, title, option1, option2, user):
    super().__init__(timeout = None)
    self.option_one = option1
    self.option_one_votes = 0
    self.option_two = option2
    self.option_two_votes = 0
    self.title = title
    self.embed = discord.Embed(title = title, color = discord.Color.red())
    self.embed.add_field(name = "Option 1", value = f"{option1}\n\nVotes: 0")
    self.embed.add_field(name = "Option 2", value = f"{option2}\n\nVotes: 0")
    self.option_one_list = []
    self.option_two_list = []
    self.is_closed = False
    self.user = user
  @discord.ui.button(label = "Option 1", style = discord.ButtonStyle.blurple)
  async def button1(self, interaction:discord.Interaction, button: discord.ui.Button):
    if not self.is_closed:
      if interaction.user.id not in self.option_one_list and interaction.user.id not in self.option_two_list:
        self.option_one_votes += 1
        embed = discord.Embed(title = self.title, color = discord.Color.red())
        embed.add_field(name = "Option 1", value = f"{self.option_one}\n\nVotes: {self.option_one_votes}")
        embed.add_field(name = "Option 2", value = f"{self.option_two}\n\nVotes: {self.option_two_votes}")
        await interaction.response.edit_message(embed = embed)
        self.option_one_list.append(interaction.user.id)
      elif interaction.user.id in self.option_one_list:
        await interaction.response.defer()
      elif interaction.user.id in self.option_two_list:
        self.option_one_votes += 1
        self.option_two_votes -= 1
        embed = discord.Embed(title = self.title, color = discord.Color.red())
        embed.add_field(name = "Option 1", value = f"{self.option_one}\n\nVotes: {self.option_one_votes}")
        embed.add_field(name = "Option 2", value = f"{self.option_two}\n\nVotes: {self.option_two_votes}")
        await interaction.response.edit_message(embed = embed)
        self.embed = embed
        self.option_two_list.remove(interaction.user.id)
        self.option_one_list.append(interaction.user.id)
    else:
      await interaction.response.defer()
  @discord.ui.button(label = "Option 2", style = discord.ButtonStyle.blurple)
  async def button2(self, interaction:discord.Interaction, button: discord.ui.Button):
    if not self.is_closed:
      if interaction.user.id not in self.option_one_list and interaction.user.id not in self.option_two_list:
        self.option_two_votes += 1
        embed = discord.Embed(title = self.title, color = discord.Color.red())
        embed.add_field(name = "Option 1", value = f"{self.option_one}\n\nVotes: {self.option_one_votes}")
        embed.add_field(name = "Option 2", value = f"{self.option_two}\n\nVotes: {self.option_two_votes}")
        await interaction.response.edit_message(embed = embed)
        self.option_one_list.append(interaction.user.id)
      elif interaction.user.id in self.option_two_list:
        await interaction.response.defer()
      elif interaction.user.id in self.option_one_list:
        self.option_one_votes -= 1
        self.option_two_votes += 1
        embed = discord.Embed(title = self.title, color = discord.Color.red())
        embed.add_field(name = "Option 1", value = f"{self.option_one}\n\nVotes: {self.option_one_votes}")
        embed.add_field(name = "Option 2", value = f"{self.option_two}\n\nVotes: {self.option_two_votes}")
        await interaction.response.edit_message(embed = embed)
        self.option_two_list.append(interaction.user.id)
        self.option_one_list.remove(interaction.user.id)
        self.embed = embed
    else:
      await interaction.response.defer()
  @discord.ui.button(label = "Close Poll", style = discord.ButtonStyle.red)
  async def closebutton(self, interaction:discord.Interaction, button:discord.Button):
    if interaction.user.__eq__(self.user) and not self.is_closed:
      self.is_closed = True
      await interaction.response.send_message(f'{self.user.mention}\'s poll has been finished. Here are the results!', embed = self.embed)
    else:
      await interaction.response.defer()
    
class threePollButtons(discord.ui.View):
  def __init__(self, title, option1, option2, option3, user):
    super().__init__(timeout = None)
    self.option_one = option1
    self.option_one_votes = 0
    self.option_two = option2
    self.option_two_votes = 0
    self.option_three = option3
    self.option_three_votes = 0
    self.title = title
    self.embed = discord.Embed(title = title, color = discord.Color.red())
    self.embed.add_field(name = "Option 1", value = f"{option1}\n\nVotes: 0")
    self.embed.add_field(name = "Option 2", value = f"{option2}\n\nVotes: 0")
    self.embed.add_field(name = "Option 3", value = f"{option3}\n\nVotes: 0")
    self.option_one_list = []
    self.option_two_list = []
    self.option_three_list = []
    self.is_closed = False
    self.user = user
  @discord.ui.button(label = "Option 1", style = discord.ButtonStyle.blurple)
  async def button1(self, interaction:discord.Interaction, button: discord.ui.Button):
    if not self.is_closed:
      if interaction.user.id not in self.option_one_list and interaction.user.id not in self.option_two_list and interaction.user.id not in self.option_three_list:
        self.option_one_votes += 1
        embed = discord.Embed(title = self.title, color = discord.Color.red())
        embed.add_field(name = "Option 1", value = f"{self.option_one}\n\nVotes: {self.option_one_votes}")
        embed.add_field(name = "Option 2", value = f"{self.option_two}\n\nVotes: {self.option_two_votes}")
        embed.add_field(name = "Option 3", value = f"{self.option_three}\n\nVotes: {self.option_three_votes}")
        await interaction.response.edit_message(embed = embed)
        self.option_one_list.append(interaction.user.id)
      elif interaction.user.id in self.option_one_list:
        await interaction.response.defer()
      elif interaction.user.id in self.option_two_list:
        self.option_one_votes += 1
        self.option_two_votes -= 1
        embed = discord.Embed(title = self.title, color = discord.Color.red())
        embed.add_field(name = "Option 1", value = f"{self.option_one}\n\nVotes: {self.option_one_votes}")
        embed.add_field(name = "Option 2", value = f"{self.option_two}\n\nVotes: {self.option_two_votes}")
        embed.add_field(name = "Option 3", value = f"{self.option_three}\n\nVotes: {self.option_three_votes}")
        await interaction.response.edit_message(embed = embed)
        self.embed = embed
        self.option_two_list.remove(interaction.user.id)
        self.option_one_list.append(interaction.user.id)
      elif interaction.user.id in self.option_three_list:
        self.option_one_votes += 1
        self.option_three_votes -= 1
        embed = discord.Embed(title = self.title, color = discord.Color.red())
        embed.add_field(name = "Option 1", value = f"{self.option_one}\n\nVotes: {self.option_one_votes}")
        embed.add_field(name = "Option 2", value = f"{self.option_two}\n\nVotes: {self.option_two_votes}")
        embed.add_field(name = "Option 3", value = f"{self.option_three}\n\nVotes: {self.option_three_votes}")
        await interaction.response.edit_message(embed = embed)
        self.embed = embed
        self.option_three_list.remove(interaction.user.id)
        self.option_one_list.append(interaction.user.id)
    else:
      await interaction.response.defer()
  @discord.ui.button(label = "Option 2", style = discord.ButtonStyle.blurple)
  async def button2(self, interaction:discord.Interaction, button: discord.ui.Button):
    if not self.is_closed:
      if interaction.user.id not in self.option_one_list and interaction.user.id not in self.option_two_list and interaction.user.id not in self.option_three_list:
        self.option_two_votes += 1
        embed = discord.Embed(title = self.title, color = discord.Color.red())
        embed.add_field(name = "Option 1", value = f"{self.option_one}\n\nVotes: {self.option_one_votes}")
        embed.add_field(name = "Option 2", value = f"{self.option_two}\n\nVotes: {self.option_two_votes}")
        embed.add_field(name = "Option 3", value = f"{self.option_three}\n\nVotes: {self.option_three_votes}")
        await interaction.response.edit_message(embed = embed)
        self.option_two_list.append(interaction.user.id)
      elif interaction.user.id in self.option_two_list:
        await interaction.response.defer()
      elif interaction.user.id in self.option_one_list:
        self.option_one_votes -= 1
        self.option_two_votes += 1
        embed = discord.Embed(title = self.title, color = discord.Color.red())
        embed.add_field(name = "Option 1", value = f"{self.option_one}\n\nVotes: {self.option_one_votes}")
        embed.add_field(name = "Option 2", value = f"{self.option_two}\n\nVotes: {self.option_two_votes}")
        embed.add_field(name = "Option 3", value = f"{self.option_three}\n\nVotes: {self.option_three_votes}")
        await interaction.response.edit_message(embed = embed)
        self.option_two_list.append(interaction.user.id)
        self.option_one_list.remove(interaction.user.id)
        self.embed = embed
      elif interaction.user.id in self.option_three_list:
        self.option_three_votes -= 1
        self.option_two_votes += 1
        embed = discord.Embed(title = self.title, color = discord.Color.red())
        embed.add_field(name = "Option 1", value = f"{self.option_one}\n\nVotes: {self.option_one_votes}")
        embed.add_field(name = "Option 2", value = f"{self.option_two}\n\nVotes: {self.option_two_votes}")
        embed.add_field(name = "Option 3", value = f"{self.option_three}\n\nVotes: {self.option_three_votes}")
        await interaction.response.edit_message(embed = embed)
        self.option_two_list.append(interaction.user.id)
        self.option_three_list.remove(interaction.user.id)
        self.embed = embed
    else:
      await interaction.response.defer()
  @discord.ui.button(label = "Option 3", style = discord.ButtonStyle.blurple)
  async def button3(self, interaction:discord.Interaction, button: discord.ui.Button):
    if not self.is_closed:
      if interaction.user.id not in self.option_one_list and interaction.user.id not in self.option_two_list and interaction.user.id not in self.option_three_list:
        self.option_three_votes += 1
        embed = discord.Embed(title = self.title, color = discord.Color.red())
        embed.add_field(name = "Option 1", value = f"{self.option_one}\n\nVotes: {self.option_one_votes}")
        embed.add_field(name = "Option 2", value = f"{self.option_two}\n\nVotes: {self.option_two_votes}")
        embed.add_field(name = "Option 3", value = f"{self.option_three}\n\nVotes: {self.option_three_votes}")
        await interaction.response.edit_message(embed = embed)
        self.option_three_list.append(interaction.user.id)
      elif interaction.user.id in self.option_three_list:
        await interaction.response.defer()
      elif interaction.user.id in self.option_one_list:
        self.option_one_votes -= 1
        self.option_three_votes += 1
        embed = discord.Embed(title = self.title, color = discord.Color.red())
        embed.add_field(name = "Option 1", value = f"{self.option_one}\n\nVotes: {self.option_one_votes}")
        embed.add_field(name = "Option 2", value = f"{self.option_two}\n\nVotes: {self.option_two_votes}")
        embed.add_field(name = "Option 3", value = f"{self.option_three}\n\nVotes: {self.option_three_votes}")
        await interaction.response.edit_message(embed = embed)
        self.option_three_list.append(interaction.user.id)
        self.option_one_list.remove(interaction.user.id)
        self.embed = embed
      elif interaction.user.id in self.option_two_list:
        self.option_three_votes += 1
        self.option_two_votes -= 1
        embed = discord.Embed(title = self.title, color = discord.Color.red())
        embed.add_field(name = "Option 1", value = f"{self.option_one}\n\nVotes: {self.option_one_votes}")
        embed.add_field(name = "Option 2", value = f"{self.option_two}\n\nVotes: {self.option_two_votes}")
        embed.add_field(name = "Option 3", value = f"{self.option_three}\n\nVotes: {self.option_three_votes}")
        await interaction.response.edit_message(embed = embed)
        self.option_three_list.append(interaction.user.id)
        self.option_two_list.remove(interaction.user.id)
        self.embed = embed
    else:
      await interaction.response.defer()
  @discord.ui.button(label = "Close Poll", style = discord.ButtonStyle.red)
  async def closebutton(self, interaction:discord.Interaction, button:discord.Button):
    if interaction.user.__eq__(self.user) and not self.is_closed:
      self.is_closed = True
      await interaction.response.send_message(f'{self.user.mention}\'s poll has been finished. Here are the results!', embed = self.embed)
    else:
      await interaction.response.defer()
  
#-----------------------------------------------------------------------------------------------
bot.run(TOKEN)
