import discord, os, sys, requests, colorama, base64
import psutil, time, json, datetime, asyncio
import smtplib
from discord.ext import commands, tasks
from colorama import Fore, init
from itertools import cycle
from email.message import EmailMessage
init()

path = os.path.dirname(os.path.abspath(__file__))
config = json.load(open(path + '/config.json'))
token = config.get('secret-spork-hax')
prefix = config.get('prefix')
owner = config.get('owner')

start_time = datetime.datetime.utcnow()

client = discord.Client()
client = commands.Bot(
	command_prefix = commands.when_mentioned_or(prefix),
	case_insensitive = True,
	intents = discord.Intents.all()
)
client.remove_command('help')

client.first_start = True

R = Fore.RED
C = Fore.CYAN
M = Fore.MAGENTA

def restart_program():
	python = sys.executable
	os.execl(python, python, * sys.argv)

def ms():
	os.system('mode con: cols=80 lines=25')
	os.system('title Moyai2021 Bot')
	os.system('cls')
	print(f'{M}[{C}Status{M}]{C}: {C}Bot is online!{M}!\n--------------------------------------------------------------------------------' + Fore.RESET)

@client.event
async def on_connect():
	ms()
	if client.first_start:
		client.first_start = False
		change_status.start()

@tasks.loop(seconds = 7200)
async def change_status():
	status_msg = f' over {len(client.guilds)} servers!'
	await client.change_presence(status = discord.Status.dnd, activity = discord.Activity(type = discord.ActivityType.watching, name = status_msg))

@client.event
async def on_message_edit(before, after):
	await client.process_commands(after)

@client.event
async def on_message(message):
	sender = message.author
	dontLog = [770072464767713280, 639778083385376768, 675448036163452959, 280689427951386624]
	channel = client.get_channel(826913791979683903)
	if isinstance(message.channel, discord.DMChannel):
		if sender.id in dontLog:
			return
		else:
			if message.attachments:
				file = message.attachments[0]
				await channel.send(f"`{sender.id} | {sender}` sent an image/file: ")
				await channel.send(file.url)
			elif message.content == '@everyone':
				await channel.send(f"`{sender.id} | {sender}` sent: {message.content.replace('@everyone', '@/everyone')}")
			elif message.content == '@here':
				await channel.send(f"`{sender.id} | {sender}` sent: {message.content.replace('@here', '@/here')}")
			else:	
				await channel.send(f"`{sender.id} | {sender}` sent: {message.content}")
	await client.process_commands(message)

@client.command()
async def dm(ctx, user_id: discord.User = None, *, msg: str = None):
	await ctx.message.delete()
	sender = ctx.author
	if sender.id in owner:
		if user_id is None:
			await ctx.send(f"`Usage: {prefix}dm <user> <message>`")
			return
		elif msg is None:
			await ctx.send(f"`Usage: {prefix}dm <user> <message>`")
			return
		await user_id.send(msg)
		print(f"{ctx.author.name} Sent a DM saying '{msg}' to {user_id.name}#{user_id.discriminator}.")
	else:
		await ctx.send("You can't do this!")

@client.command(aliases = ['m'])
async def module(ctx, option = None, extention = None):
	sender = ctx.author
	if sender.id == 353340381359767552:
		await ctx.message.delete()
		if option is None:
			await ctx.send(f'`Usage: {prefix}module <load[l]/unload[u]/reload[r]> <module>`')
			return
		elif option == 'l':
			client.load_extension(f'cogs.{extention}')
			print(f'Loaded {extention} cog!')
		elif option == 'u':
			client.unload_extension(f'cogs.{extention}')
			print(f'Unloaded {extention} cog!')
		elif option == 'r':
			if extention == 'all':
				for filename in os.listdir('./cogs'):
					if filename.endswith('.py'):
						client.reload_extension(f'cogs.{filename[:-3]}')
				print('Reloaded all cogs!')
			else:
				client.reload_extension(f'cogs.{extention}')
				print(f'Reloaded {extention} cog!')
	else:
		return

@client.command()
async def help(ctx):
		Main = f'''`{prefix}dm` - Direct messages someone within a server. 
`{prefix}shutdown` - This command only works for the owner of the bot. This command shutsdown the bot program.
`{prefix}restart` - This command only works for the owner of the bot. This command restarts the bot program.'''
		Fun = f'''`{prefix}em` - embeds the message.
`{prefix}av` - shows the avatar of a user pinged. 
`{prefix}roll` - Picks a random number from 1 to 100. 
`{prefix}spam` - Spam a message you want to send with the amount after the message.
`{prefix}zawarudo` - Sends a message saying "The World, time has frozen" in bold.'''
		Network = f'''`{prefix}email` - Send an email to the developer account.'''
		Info = f'''`{prefix}Hey` - Sends a message saying "Fuck you!".
`{prefix}ping` - Shows the client latency.
`{prefix}info` - Shows information about the bot.
`{prefix}status` - Shows client latency, API latency, uptime, and Discord/Python versions.
`{prefix}whois` - shows information about a user.'''
		em = discord.Embed(title = "Help Commands", description = f'`{prefix}help` - shows this command', colour = discord.Color.random())
		em.add_field(name = 'Main', value = Main, inline = True)
		em.add_field(name = 'Fun', value = Fun, inline = True)
		em.add_field(name = 'Network', value = Network, inline = True)
		em.add_field(name = 'Info', value = Info, inline = True)
		em.set_footer(text = "Email Jrboone2017@aol.com if you are experiencing any issues with the bot.")
		await ctx.send(embed=em)

@client.command()
@commands.is_owner()
async def Restart(ctx):
	await ctx.message.delete()
	message = await ctx.send("Restarting bot... Wait a couple seconds!")
	restart_program()

@client.command()
@commands.is_owner()
async def Shutdown(ctx):
	message = await ctx.send("Bot is offline!")
	await client.close()

for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f'cogs.{filename[:-3]}')

client.run("ODY1MTM5MTg0MTM4MzIxOTMw.YO_ppw.Uvzu9F0STv4UdzDqz10jyxx4Yp0")