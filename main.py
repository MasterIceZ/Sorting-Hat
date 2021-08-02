import discord
from discord.ext import commands
import os
import asyncio
from numpy.random import choice
from runner import alive

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

alive()
client.run(token)