#!~/.venvs/3.12/bin/python3.12
import selfcord
from selfcord.ext import tasks
import os
import yaml
import random
import asyncio
import sys
import requests
import traceback

from utils import getconfig
from utils import webhooks

os.chdir(os.path.dirname(os.path.abspath(__file__)))

config = getconfig.get()

error_handler = webhooks.makeObject(config['urls']['own8'])

# Redirect stderr to the webhook handler
sys.stderr = error_handler

client = selfcord.Client()

@client.event
async def on_ready():
    await asyncio.sleep(20)
    task1.start()
    print('ready own8')


@tasks.loop(minutes=0.5)
async def task1():
    for serverid in config['servers8']:
        try:
            guild = client.get_guild(serverid)
            if guild is None:
                guild = await client.fetch_guild(serverid)
            channel = guild.text_channels[0]
            await channel.send(random.randint(1,1000))
            await asyncio.sleep(2)
        except Exception as e:
            print()
            print(e)
            print()

@client.event
async def on_command_error(ctx, error):
    print(f'<@{config['your_user_id']}> Command error: `{error}`', file=sys.stderr)  # Print error to stderr

@client.event
async def on_error(event, *args, **kwargs):
    exc_type, exc_value, exc_tb = sys.exc_info()
    error_message = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print(f'<@{config['your_user_id']}> An error occurred: `{error_message}`', file=sys.stderr)  # Print error to stderr

client.run(config['tokens']['own8'])
