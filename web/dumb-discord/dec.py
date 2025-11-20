# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: server.py
# Bytecode version: 3.6rc1 (3379)
# Source timestamp: 2020-12-02 02:30:35 UTC (1606876235)

from discord.ext import commands
import discord
import json
from discord.utils import get

def obfuscate(byt):
    mask = b'ctf{tryharderdontstring}'
    lmask = len(mask)
    return bytes((c ^ mask[i % lmask] for i, c in enumerate(byt)))

def test(s):
    data = obfuscate(s.encode())
    return data
intents = discord.Intents.default()
intents.members = True
cfg = open('config.json', 'r')
tmpconfig = cfg.read()
cfg.close()
config = json.loads(tmpconfig)
token = config["token"]
client = commands.Bot(command_prefix='/')

@client.event
async def on_ready():
    print('Connected to bot: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))

@client.command()
async def getflag(ctx):
    await ctx.send(test('\x13\x1b\x08\x1c').decode())

@client.event
async def on_message(message):
    await client.process_commands(message)
    if "!ping" in message.content.lower():
        await message.channel.send("pong")
    if "getflag" in message.content.lower() and message.author.id == 783473293554352141:
        role = discord.utils.get(message.author.guild.roles, name="dctf2020.cyberedu.ro")
        member = discord.utils.get(message.author.guild.members, id=message.author.id)
        if role in member.roles:
            await message.channel.send(test(config["flag"]))
    if "help" in message.content.lower():
        await message.channel.send("Try harder!")
    if '/s基ay' in message.content.lower():
        await message.channel.send(message.content.replace('/s基ay', '').replace("/getflag", ''))
client.run(token)