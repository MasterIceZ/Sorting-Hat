import discord
from discord.ext import commands
import os
import asyncio
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
	if msg.content.startswith('?unmute'):
		await msg.add_reaction('👍')

@client.event
async def on_raw_reaction_add(payload):
	if payload.emoji.name == '👍':
		chan = client.get_channel(867366262716104724)
		msg = await chan.fetch_message(payload.message_id)
		reaction = get(msg.reactions, emoji=payload.emoji.name)
		print(reaction)
		if reaction and reaction.count >= 4:
			target = msg.content.split()[1].split('<@!')[1].split('>')[0]
			print(target)
			tar = str()
			for person in chan.members:
				if str(person.id) == str(target):
					tar = person
					print('found')
					break
			print(msg.content.split()[0])
			if msg.content.split()[0] == '?mute':
				await tar.edit(mute=True)
				await msg.delete()
			elif msg.content.split()[0] == '?unmute':
				await tar.edit(mute=False)
				await msg.delete()

alive()
client.run(token)
