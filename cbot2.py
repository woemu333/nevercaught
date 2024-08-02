#!~/.venvs/3.12/bin/python3.12
import selfcord
from selfcord.ext import tasks
import os
import yaml
import random
import asyncio

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def getconfig():
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)
    return config
config = getconfig()

client = selfcord.Client()

@client.event
async def on_ready():
    await asyncio.sleep(15)
    task1.start()
    print('ready')


@tasks.loop(minutes=0.5)
async def task1():
    for serverid in config['server_ids']:
        guild = client.get_guild(serverid)
        channel = guild.text_channels[0]
        await channel.send(random.randint(1,1000))
        await asyncio.sleep(8)

client.run(config['token2'])
