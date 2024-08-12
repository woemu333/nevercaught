#!~/.venvs/3.12/bin/python3.12
import selfcord
from selfcord.ext import tasks
from discord_webhook import DiscordWebhook
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
    print('ready storage')
webhookurl = 'https://discord.com/api/webhooks/1268374793040695316/2trCno1syYd4r2l9uUXlCT3MqGF4BS9Rl0s9_TwEZ8zlOxnxCUMIvOUBOsHqTDV8tfya'

with open('rarity.txt','r+') as f:
    raritylist = f.readlines()

ballsdex_userid = 999736048596816014
@client.event
async def on_message(message: selfcord.Message):
    
    if 'give ' in message.content and message.author.id == 707866373602148363:
        hexid = message.content.split(' ',1)[1]
        if hexid[0] == '#':
            hexid = hexid[1:]
        commands = [command async for command in message.channel.slash_commands()]
        for command in commands:
            if command.name == 'balls':
                for subcommand in command.children:
                    if subcommand.name == 'give':
                        give = await subcommand.__call__(channel=message.channel, user=message.author, countryball=int(hexid, 16))
                        break
                break
        await asyncio.sleep(2)
        givemessage = give.message.content
        try:
            emoji = f'<{givemessage.split('<',1)[1].split('>',1)[0]}>'
        except IndexError:
            await message.channel.send(f'I don\'t have the ball with id {hexid}')
    




    if 'count ' in message.content:
        inputball = message.content.split(' ',1)[1]
        print(inputball)
        
        if inputball.upper() == 'ALL':
            commands = [command async for command in message.channel.slash_commands()]
            for command in commands:
                if command.name == 'balls':
                    for subcommand in command.children:
                        if subcommand.name == 'count':
                            countmessage = await subcommand.__call__(channel=message.channel)
                            break
                    break
            await asyncio.sleep(2)
            count = countmessage.message.content
            count = count.split(' ')[2]
            await message.channel.send(f'I have {count} countryballs')
        


        else:
            realballnumber = None
            found = False
            for ball in raritylist:
                temp = ball.split('. ',2)
                ballnumber = temp[1]

                ballname = temp[2].replace('\n','')
                if inputball.upper() == ballname.upper():
                    print(ballnumber)
                    print(inputball)
                    print(ballname)
                    realballnumber = ballnumber
                    inputball = ballname
                    found = True
                    break
            if not found:
                await message.channel.send(f'That\'s not a countryball')

            commands = [command async for command in message.channel.slash_commands()]
            for command in commands:
                if command.name == 'balls':
                    for subcommand in command.children:
                        if subcommand.name == 'count':
                            print(realballnumber)
                            countmessage = await subcommand.__call__(channel=message.channel, countryball=int(realballnumber))
                            break
                    break
            await asyncio.sleep(2)
            count = countmessage.message.content
            count = count.split(' ')[2]
            await message.channel.send(f'I have {count} {inputball} countryballs')





    if 'rarity ' in message.content:
        inputball = message.content.split(' ',1)[1]
        for ball in raritylist:
            temp = ball.split('. ',1)
            rarity = temp[0]
            ballname = temp[1].replace('\n','')
            if inputball == ballname:
                await message.channel.send(f'{inputball} is a top {rarity}')
                break
        

client.run(config['tokens']['storage'])
