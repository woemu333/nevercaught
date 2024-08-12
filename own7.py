#!~/.venvs/3.12/bin/python3.12
import selfcord
from selfcord.ext import tasks
import os
import yaml
import random
import asyncio

from utils import getconfig

os.chdir(os.path.dirname(os.path.abspath(__file__)))

config = getconfig.get()

client = selfcord.Client()

@client.event
async def on_ready():
    await asyncio.sleep(15)
    task1.start()
    print('ready own7')


@tasks.loop(minutes=0.5)
async def task1():
    for serverid in config['servers7']:
        guild = client.get_guild(serverid)
        if guild is None:
            guild = await client.fetch_guild(serverid)
        channel = guild.text_channels[0]
        await channel.send(random.randint(1,1000))
        await asyncio.sleep(2)

client.run(config['tokens']['own7'])
