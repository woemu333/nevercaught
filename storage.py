#!~/.venvs/3.12/bin/python3.12
import selfcord
from selfcord.ext import tasks
from selfcord.ext import commands
from discord_webhook import DiscordWebhook
import os
import yaml
import random
import asyncio

from utils import getconfig

os.chdir(os.path.dirname(os.path.abspath(__file__)))

config = getconfig.get()

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('ready storage')
webhookurl = 'https://discord.com/api/webhooks/1268374793040695316/2trCno1syYd4r2l9uUXlCT3MqGF4BS9Rl0s9_TwEZ8zlOxnxCUMIvOUBOsHqTDV8tfya'

with open('rarity.txt','r+') as f:
    raritylist = f.readlines()

ballsdex_userid = 999736048596816014

@bot.event
async def on_message(message):
    # Prevent bot from responding to its own messages
    if message.author == bot.user:
        return

    # Add any additional custom logic here

    # Process commands (necessary for the command handler to recognize commands)
    await bot.process_commands(message)

@bot.command(name='give')
async def _give(ctx: commands.Context, hexid):
    if ctx.author.id == 707866373602148363:
        if hexid[0] == '#':
            hexid = hexid[1:]
        commands = await ctx.channel.application_commands()
        for command in commands:
            if command.name == 'balls':
                for subcommand in command.children:
                    if subcommand.name == 'give':
                        give = await subcommand.__call__(channel=ctx.channel, user=ctx.author, countryball=int(hexid, 16))
                        break
                break
        await asyncio.sleep(1)
        givectx = give.message.content
        try:
            emoji = f'<{givectx.split('<',1)[1].split('>',1)[0]}>'
        except IndexError:
            await ctx.send(f'I don\'t have the ball with id {hexid}')

@bot.command(name='info')
async def _info(ctx: commands.Context, hexid):
    if hexid[0] == '#':
        hexid = hexid[1:]
    commands = await ctx.channel.application_commands()
    for command in commands:
        if command.name == 'balls':
            for subcommand in command.children:
                if subcommand.name == 'info':
                    give = await subcommand.__call__(channel=ctx.channel, countryball=int(hexid, 16))
                    break
            break
    await asyncio.sleep(1)
    givectx = give.message.content
    print(givectx)
    if 'The countryball could not be found' in givectx or 'That countryball doesn\'t belong to you' in givectx:
        await ctx.send(f'I don\'t have the ball with id {hexid}')

@bot.command(name='last')
async def _last(ctx: commands.Context):
    commands = await ctx.channel.application_commands()
    for command in commands:
        if command.name == 'balls':
            for subcommand in command.children:
                if subcommand.name == 'last':
                    give = await subcommand.__call__(channel=ctx.channel)
                    break
            break
    # await asyncio.sleep(1)
    # givectx = give.message.content
    # print(givectx)
    # if 'The countryball could not be found' in givectx or 'That countryball doesn\'t belong to you' in givectx:
    #     await ctx.send(f'I don\'t have the ball with id {hexid}')

@bot.command(name='count')
async def _count(ctx: commands.Context, *, inputball: str):
    # inputball = message.content.split(' ',1)[1]
    print(inputball)
    
    if inputball.upper() == 'ALL':
        commands = await ctx.channel.application_commands()
        for command in commands:
            if command.name == 'balls':
                for subcommand in command.children:
                    if subcommand.name == 'count':
                        countmessage = await subcommand.__call__(channel=ctx.channel)
                        break
                break
        await asyncio.sleep(1)
        count = countmessage.message.content
        count = count.split(' ')[2]
        await ctx.send(f'I have {count} countryballs')
    
    elif inputball.upper() == 'RICHNESS':
        progress = await ctx.send(f'Adding up the values:\n`(----------------) 00.00%`')

        top11list = []
        for ball in raritylist:
            temp = ball.split('. ',2)
            ballnumber = temp[1]
            ballrarity = temp[0]

            ballname = temp[2].replace('\n','')
            # print(ballnumber)
            if int(ballrarity) <= 11:
                top11list.append([int(ballrarity),int(ballnumber)])
            else:
                break
        top11list.append('shiny')

        givecommand = None
        commands = await ctx.channel.application_commands()
        for command in commands:
            if command.name == 'balls':
                for subcommand in command.children:
                    if subcommand.name == 'count':
                        givecommand = subcommand
                        break
                break

        richnesslist = []
        i = 0
        # progress = await ctx.message
        for ball in top11list:
            i += 1
            if i != 17:
                await progress.edit(f'Adding up the values:\n`({'#'*i}{'-'*(16-i)}) {round(i/16*100,2)}%`')
            else:
                await progress.edit(f'Calculating...')
            if ball == 'shiny':
                countmessage = await givecommand.__call__(channel=ctx.channel,shiny='true')
            else: 
                countmessage = await givecommand.__call__(channel=ctx.channel,countryball=int(ball[1]))
            await asyncio.sleep(1)
            count = countmessage.message.content
            print(count)
            count = count.split(' ')[2]
            if ball == 'shiny':
                richnesslist.append([5,int(count)])
            else:
                richnesslist.append([ball[0],int(count)])
        
        values = {
            1:1,
            4:0.8,
            5:0.5,
            7:0.4,
            8:0.3,
            9:0.2,
            10:0.15,
            11:0.1
        }

        rich = 0
        for ball in richnesslist:
            rich += values[ball[0]]*ball[1]
        
        rich = round(rich, 2)
        
        await ctx.send(f'I am worth `{rich}` top 1s')



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
            await ctx.send(f'That\'s not a countryball')

        commands = await ctx.channel.application_commands()
        for command in commands:
            if command.name == 'balls':
                for subcommand in command.children:
                    if subcommand.name == 'count':
                        print(realballnumber)
                        countmessage = await subcommand.__call__(channel=ctx.channel, countryball=int(realballnumber))
                        break
                break
        await asyncio.sleep(1)
        count = countmessage.message.content
        count = count.split(' ')[2]
        await ctx.send(f'I have {count} {inputball} countryballs')




@bot.command(name='rarity')
async def _rare(ctx: commands.Context, *, inputball: str):
        # inputball = message.content.split(' ',1)[1]
    for ball in raritylist:
        temp = ball.split('. ',2)
        rarity = temp[0]
        ballname = temp[2].replace('\n','')
        if inputball.upper() == ballname.upper():
            await ctx.send(f'{ballname} is a top {rarity}')
            break
        

bot.run(config['tokens']['storage'])
