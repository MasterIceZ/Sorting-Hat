import discord
from discord.ext import commands
import os
from numpy.random import choice
from runner import alive

from discord.utils import get

token = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = "?", intents = intents)

hu = [
	'Gryffindor',
	'Ravenclaw',
	'Hufflepuff',
	'Slytherin'
]

rate = [0.22, 0.26, 0.26, 0.26]

@client.event
async def on_ready() :
	print("Hello Ice")
	await client.change_presence(activity = discord.Activity(type=discord.ActivityType.watching, name="Harry Potter"))

@client.event
async def on_member_join(member):
	print('ok')
	rl = choice(hu, p=rate)
	print(member)
	cha = client.get_channel(867332516277125163)
	st = 'ยินดีต้อนรับ' + member.mention + 'เข้าสู่บ้าน ' + rl
	role = discord.utils.get(member.guild.roles, name=rl)
	await member.add_roles(role)
	await cha.send(st)

@client.event
async def on_message(msg):
	if msg.author == client.user :
		return
	if msg.content.startswith('?mute'):
		await msg.add_reaction('👍')
		await msg.add_reaction('👎')
	if msg.content.startswith('?unmute'):
		await msg.add_reaction('👍')
		await msg.add_reaction('👎')
@client.event
async def on_raw_reaction_add(payload):
	if payload.emoji.name == '👍':
		chan = client.get_channel(867366262716104724)
		msg = await chan.fetch_message(payload.message_id)
		reaction = get(msg.reactions, emoji=payload.emoji.name)
		print(msg.content.split()[1])
		if reaction and reaction.count >= 4:
			if msg.content.split()[0] == '?mute' or msg.content.split()[0] == '?unmute':
				target = msg.content.split()[1].split('<@')[1].split('>')[0]
			else :
				return
			print(target)
			tar = str("NOT")
			p = False
			if target.startswith('!'):
				p = True
				target = target.split('!')[1]
			else :
				p = False
				target = target.split('&')[1]
			
			if p == True:
				for person in chan.members:
					if str(person.id) == str(target):
						tar = person
						break
				if tar == "NOT":
					return 
				print(msg.content.split()[0])
				if msg.content.split()[0] == '?mute':
					try:
						await tar.edit(mute=True)
					except:
						pass
					
				elif msg.content.split()[0] == '?unmute':
					try:
						await tar.edit(mute=False)
					except:
						pass
				await msg.delete()
			else :
				tg = get(chan.guild.roles, id=int(target))
				for person in chan.members:
					if tg in person.roles:
						if msg.content.split()[0] == '?mute':
							try:
								await person.edit(mute=True)
							except:
								pass
						elif msg.content.split()[0] == '?unmute':
							try:
								await person.edit(mute=False)
							except:
								pass
				await msg.delete()
	elif payload.emoji.name == '👎':
		chan = client.get_channel(867366262716104724)
		msg = await chan.fetch_message(payload.message_id)
		reaction = get(msg.reactions, emoji=payload.emoji.name)
		com = msg.content.split()[0]
		if reaction and reaction.count >= 4:
			if com == '?mute' or com == '?unmute':
				try:
					await msg.delete()
				except:
					pass

alive()
client.run(token)
