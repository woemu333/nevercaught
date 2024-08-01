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
    task1.start()
    print('ready')

serveridlist = [1268358108942696481,1268358043846971393,1268357963148558480]


@tasks.loop(minutes=1)
async def task1():
    for serverid in serveridlist:
        await asyncio.sleep(2)
        guild = client.get_guild(serverid)
        channel = guild.text_channels[0]
        await channel.send(random.randint(1,1000))

client.run(config['bot']['token2'])
