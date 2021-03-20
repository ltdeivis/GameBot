#Discord Bot
import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
from game.game_room import GameRoom

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

gameDict = {}

intents = discord.Intents.all()
bot = discord.ext.commands.Bot(command_prefix='.', intents=intents)

@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Activity(name="you", type=discord.ActivityType.watching), status=discord.Status.dnd)
	print("*Menacing* game Bot has woken up")

@bot.command()
async def createRoom(ctx):
	# Get reference to the guild
	guild = ctx.message.guild

	# Check it exists
	if guild is None:
		return

	# Get game channel category
	category = discord.utils.get(guild.categories, name="Game Rooms")

	# Check there's players in mentions
	if len(ctx.message.mentions) < 1:
		return

	# Get each players id from mentions
	playerIDs = []
	for mention in ctx.message.mentions:
		playerIDs.append(mention.id)

	# Also add author to the list
	playerIDs.append(ctx.author.id)

	# Member object list for players
	players = []

	# Check that each player and author is eligible to create a room
	playersValid = True
	for pId in playerIDs:
		# Get member object using user ID
		player = discord.utils.get(bot.get_all_members(), id=pId)

		# Check player is not None
		if not player:
			playersValid = False
			break

		# Check player does not have role starting with game-Room-
		for role in player.roles:
			if role.name[0:10] == "game-room-":
				playersValid = False
				break

		# Player is valid so add him to list of member objects
		players.append(player)

	if playersValid == False:
		await ctx.send("Mentioned players were not valid")
		return

	# Ensure room name is unique
	channelName = ""
	validName = False
	while validName == False:
		# Create random channel name
		channelID = random.randint(1, 10000)
		channelName = "game-room-" + str(channelID)

		# Check game room name doesn't exist already
		for channel in guild.text_channels:
			if channelName != channel:
				validName = True
			else:
				validName = False

	print(f'Creating {channelName} channel...')

	# Create temporary role
	role = channelName + "-player"
	authorizedRole = await guild.create_role(name=role, hoist=True)

	# Create overwrites to allow only authorized users to use room
	overwrites = {
		guild.default_role: discord.PermissionOverwrite(read_messages=False),
		authorizedRole: discord.PermissionOverwrite(read_messages=True)
	}

	# Create game room
	channel = await guild.create_text_channel(channelName, overwrites=overwrites,category=category)

	# Add game room to dictionary of open rooms
	gameDict[channelName] = GameRoom(players, channelName)
	print(f'{channelName} saved to dictionary')

	# Add new roles to players
	await ctx.author.add_roles(authorizedRole)
	for player in players:
		# Add role
		await player.add_roles(authorizedRole)

	print(f'{channelName} Created')

@bot.command()
async def endGame(ctx):
	# Get reference to the guild
	guild = ctx.message.guild

	# Check channel name where command is called from
	channel = ctx.message.channel
	if channel.name[0:10] != "game-room-":
		return

	# Get the role object from the guild
	roleObject = discord.utils.get(guild.roles, name=channel.name+"-player")

	# Delete role from the server
	await roleObject.delete()

	# Delete channel from the server
	await channel.delete()
	print(f'game room: {channel.name} Deleted')

	# Remove channel from open room dictionary
	gameDict.pop(channel.name)
	print(f'game room: {channel.name} Removed from open room list')

@bot.event
async def on_message(message):
	await bot.process_commands(message)

	# Prefix of ! will be processed by game_room
	if message.content.startswith('!'):
		# Get the room object using channel name
		room = gameDict.get(message.channel.name)
		# Check that room is within the dictionary
		if room is not None:
			output = room.process_input(message)
			if output is not None:
				channel = message.channel
				await channel.send(output)

@bot.command()
async def ping(ctx):
	await ctx.send(f'Ping: {str(int(bot.latency))}')

bot.run(TOKEN)