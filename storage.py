#!~/.venvs/3.12/bin/python3.12
import selfcord
from selfcord.ext import tasks
from selfcord.ext import commands
from discord_webhook import DiscordWebhook
import os
import yaml
import random
import asyncio
import string
import json
import sys
import requests
import traceback

from utils import getconfig
from utils import webhooks

os.chdir(os.path.dirname(os.path.abspath(__file__)))

config = getconfig.get()

error_handler = webhooks.makeObject(config['urls']['storage'],os.path.basename(__file__))

# Redirect stderr to the webhook handler
sys.stderr = error_handler

bot = commands.Bot(command_prefix='.',help_command=None)

@bot.event
async def on_ready():
    print('ready storage')
    

with open('rarity.txt','r+') as f:
    raritylist = f.readlines()

ballsdex_userid = 999736048596816014

@bot.event
async def on_message(message: selfcord.Message):
    # Prevent bot from responding to its own messages
    if message.author == bot.user:
        return

    # Add any additional custom logic here

    # Process commands (necessary for the command handler to recognize commands)
    await bot.process_commands(message)

    if message.channel.id == 1281843539369529505:
        if message.author.id == 1268101370997641291:
            if message.content == 'ping':
                await message.channel.send('pong')
    
    if message.channel.id == 1268374682516590756:
        try:
            hexid = message.content.split('(#')[1].split(',')[0]
            if 'Thailand' in message.content:
                ball = 'Thailand'
                giveuser = await bot.fetch_user(908954867962380298)
            elif 'Ukraine' in message.content:
                ball = 'Ukraine'
                giveuser = await bot.fetch_user(1239692843942019167)
            elif 'Prussia' in message.content:
                ball = 'Prussia'
                giveuser = await bot.fetch_user(1023478831560007732)
            elif 'Byelorussian Soviet Socialist Republic' in message.content:
                ball = 'Byelorussian Soviet Socialist Republic'
                giveuser = await bot.fetch_user(862981715621707787)
            else:
                return
        except selfcord.errors.Forbidden:
            return
        
        try:
            givechannel = await bot.fetch_channel(1272530030747979776)
        except selfcord.errors.Forbidden:
            DiscordWebhook(url=config['urls']['gives'], content=f'{ball} `(#{hexid})` could not be given because <@1273823384278532128> needs to be verified.').execute()
            return
        commands = await givechannel.application_commands()
        for command in commands:
            if command.name == 'balls':
                for subcommand in command.children:
                    if subcommand.name == 'give':
                        givecommand = subcommand
                        break
                break
        
        await givecommand.__call__(channel=givechannel, user=giveuser, countryball=int(hexid, 16))


@bot.command(name='give')
async def _give(ctx: commands.Context, *, arg=None):
    commands = await ctx.channel.application_commands()
    for command in commands:
        if command.name == 'balls':
            for subcommand in command.children:
                if subcommand.name == 'list':
                    listcommand = subcommand
                    break
            break
    for command in commands:
        if command.name == 'balls':
            for subcommand in command.children:
                if subcommand.name == 'give':
                    givecommand = subcommand
                    break
            break

    parsed_args = {
        'user':ctx.message.author,
        'countryball':None,
        'special':'any',
        'count':'1',
        'sort':'worst_stats',
        'file':False
    }

    args = arg
    while True:
        if args == None:
            break

        split = args[::-1].split(':')
        if split == ['']:
            break
        value = split[0][::-1].strip()
        try:
            key = split[1].split(' ',1)[0][::-1].strip()
        except IndexError:
            key = split[1][::-1].strip()
            break

        parsed_args[key] = value
        # print(parsed_args)
        args = args[:-1*len(f' {key}:{value}')]

    #user
    if parsed_args['user'] != ctx.message.author:
        try:
            user = parsed_args['user'].split('@')[1].split('>')[0]
        except IndexError:
            try:
                user = int(parsed_args['user'])
            except ValueError:
                await ctx.send(f'User not found: "{parsed_args["user"]}"')
                return
        if str(user)[0] == '&':
            await ctx.send(f'You entered a role, not a user!')
            return
        try:
            user = await bot.fetch_user(user)
        except selfcord.errors.NotFound:
            await ctx.send(f'User not found: "{parsed_args["user"]}"')
            return
        parsed_args['user'] = user

    #file
    if parsed_args['file'] != False:
        file = parsed_args['file']
        if file.lower() == 'true':
            parsed_args['file'] = True
        else:
            parsed_args['file'] = False
    
    if parsed_args['file'] != True:
        #countryball
        if parsed_args['countryball'] != None:
            if parsed_args['countryball'].upper() == 'ALL':
                parsed_args['countryball'] = 'all'
            else:
                found = False
                for ball in raritylist:
                    temp = ball.split('. ',2)

                    ballrarity = temp[0]
                    ballnumber = temp[1]
                    ballname = temp[2].replace('\n','')

                    if parsed_args['countryball'].upper() == ballname.upper():
                        parsed_args['countryball'] = [ballrarity,ballnumber,ballname]
                        found = True
                        break
                if not found:
                    await ctx.send(f'Countryball not found: "{parsed_args["countryball"]}"')
                    return
        else:
            await ctx.send(f'Please specify a countryball')
            return

        #special
        if parsed_args['special'].upper() != 'ANY':
            if parsed_args['special'].upper() == 'SHINY':
                parsed_args['special'] = 'shiny'
            elif parsed_args['special'].upper() == 'NONE':
                parsed_args['special'] = 'none'
            else:
                await ctx.send(f'Special not found: "{parsed_args["special"]}"')
                return
        else:
            parsed_args['special'] = 'any'
            
        #count
        if parsed_args['count'] != '1':
            count = parsed_args['count']
            if count[0:3].upper() == 'ALL':
                try:
                    int(count[4:])
                except ValueError or IndexError:
                    await ctx.send(f'There was an error with the count: "{parsed_args["count"]}"')
                    return
                parsed_args['count'] = count.lower()
            else:
                try:
                    int(count)
                except ValueError:
                    await ctx.send(f'There was an error with the count: "{parsed_args["count"]}"')
                    return
                parsed_args['count'] = count.lower()
        else:
            parsed_args['count'] = '1'

        #sort
        if parsed_args['sort'].replace(' ','_').upper() != 'worst_stats':
            sort = parsed_args['sort']
            options = [
                'worst_stats',
                'best_stats',
                'catch_date',
                'rarity',
                'reverse_rarity'
            ]

            if sort.replace(' ','_').lower() in options:
                parsed_args['sort'] = sort.replace(' ','_').lower()
            else:
                await ctx.send(f'Sort option not found: "{parsed_args["sort"]}"\nThe options are: worst_stats, best_stats, catch_date, rarity, reverse_rarity')
                return
        else:
            parsed_args['sort'] = 'worst_stats'

        sortdict = {
            'stats_bonus':'stats',
            'catch_date':'-catch_date',
            'rarity':'ball__rarity',
        }
        kwargs = {
            'user':bot.user,
            'sort':'',
            'reverse':False,
        }
        if parsed_args['countryball'] != 'all':
            kwargs['countryball'] = parsed_args['countryball'][1]

        'worst_stats'
        'best_stats'
        'catch_date'
        'rarity'
        'reverse_rarity'

        if parsed_args['sort'] in ['worst_stats', 'best_stats']:
            kwargs['sort'] = sortdict['stats_bonus']

        if parsed_args['sort'] == 'catch_date':
            kwargs['sort'] = sortdict['catch_date']

        if parsed_args['sort'] in ['rarity','reverse_rarity']:
            kwargs['sort'] = sortdict['rarity']

        if parsed_args['sort'] in ['worst_stats', 'reverse_rarity']:
            kwargs['reverse'] = True


        listinteraction = await listcommand.__call__(**kwargs)

        await asyncio.sleep(2)


        ballslist = [] # format: [special, id, name, [atk, hp]]

        specialdict = {
            '✨':'shiny',
            '':'none'
        }

        while True:
            if "You don't have any" in listinteraction.message.content:
                await ctx.send('You have none of this countryball')
                return
            if "This command is on cooldown" in listinteraction.message.content:
                await ctx.send(listinteraction.message.content)
                return
            if type(listinteraction.message.components[0].children[0]) == selfcord.components.SelectMenu:
                page = listinteraction.message.components[0].children[0]

                for ball in page.options:
                    
                    special = specialdict[ball.label.split('#',1)[0].strip()]
                    id = ball.label.split('#',1)[1].split(' ',1)[0]
                    name = ball.label.split('#',1)[1].split(' ',1)[1]
                    atk = ball.description.split(' • ')[0].split(' ')[1].replace('%','')
                    hp = ball.description.split(' • ')[1].split(' ')[1].replace('%','')
                    ball_details = {
                        'special':special,
                        'id':id,
                        'name':name,
                        'stats':{
                            'atk':atk,
                            'hp':hp
                        }
                    }
                    print(ball_details)
                    ballslist.append(ball_details)

                break
            else:
                page = listinteraction.message.components[2].children[0]
                button = listinteraction.message.components[0].children[3]

                for ball in page.options:
                    
                    special = specialdict[ball.label.split('#',1)[0].strip()]
                    id = ball.label.split('#',1)[1].split(' ',1)[0]
                    name = ball.label.split('#',1)[1].split(' ',1)[1]
                    atk = ball.description.split(' • ')[0].split(' ')[1].replace('%','')
                    hp = ball.description.split(' • ')[1].split(' ')[1].replace('%','')
                    ball_details = {
                        'special':special,
                        'id':id,
                        'name':name,
                        'stats':{
                            'atk':atk,
                            'hp':hp
                        }
                    }
                    print(ball_details)
                    ballslist.append(ball_details)

                if button.disabled:
                    break
                else:
                    await button.click()

        await listinteraction.message.delete()

        removelist = []
        for ball in ballslist:
            if parsed_args['special'].upper() != 'ALL':
                if parsed_args['special'] == 'shiny' and ball['special'] != 'shiny':
                    removelist.append(ball)
                elif parsed_args['special'] == 'none' and ball['special'] != 'none':
                    removelist.append(ball)

        for remove in removelist:
            ballslist.remove(remove)
        if parsed_args['count'] != 'all':
            if parsed_args['count'][0:3].upper() == 'ALL':
                count = int(parsed_args['count'][4:])
                if len(ballslist)-count < 1:
                    await ctx.send(f'I have less than {count+1} of this ball, sorry!')
                    return
                newcount = len(ballslist)-count
            else:
                count = int(parsed_args['count'])
                if len(ballslist) < count:
                    await ctx.send(f'I have less than {count} of this ball, sorry!')
                    return
                newcount = count
        else:
            newcount = 'all'
    
    else:
        newcount = 'all'
        name = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits + string.digits, k=10))
        await ctx.message.attachments[0].save(f'{name}.json')
        with open(f'{name}.json','r+') as f:
            ballslist = f.read()
            ballslist = json.loads(ballslist)
            comments = ballslist['_comments']
            ballslist = ballslist['data']
        os.remove(f'{name}.json')
        

    
    currentcount = 0
    givelist = []
    for ball in ballslist:
        currentcount+=1
        if newcount != 'all':
            if currentcount > newcount:
                break
        givelist.append(ball)
        await givecommand.__call__(user=parsed_args['user'],countryball=int(ball['id'],16))



    name = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits + string.digits, k=10))
    with open(f'{name}.json','x+') as f:
        data = {
            '_comments':{
                
            },
            'data':givelist
        }
        if parsed_args['file'] == False:
            data['_comments']['user'] = {'name':parsed_args['user'].name,'id':parsed_args['user'].id}
            data['_comments']['file'] = 'False'
            data['_comments']['countryball'] = parsed_args['countryball'][2]
            data['_comments']['special'] = parsed_args['special']
            data['_comments']['count'] = parsed_args['count']
            data['_comments']['sort'] = parsed_args['sort']
        else:
            data['_comments'] = comments
            data['_comments']['file'] = 'True'
            data['_comments']['user'] = {'name':parsed_args['user'].name,'id':parsed_args['user'].id}

        f.writelines(json.dumps(data,indent=4))

    if newcount == 'all' and parsed_args['file'] == True:
        newcount = len(ballslist)

    if parsed_args["special"].upper() not in ["ANY","NONE"]:
        special = f" {parsed_args['special'].title()}"
    else:
        special = " "

    if parsed_args['countryball'] == None:
        parsed_args['countryball'] = [None,None,'countryball']

    if type(parsed_args["countryball"]) != str:
        if parsed_args['countryball'] != [None,None,'countryball']:
            ball_name = f" {parsed_args['countryball'][2]}"
        else:
            ball_name = "countryball"
    else:
        ball_name = " "

    if newcount == "all":
        plural = "s"
    elif newcount >= 2 and parsed_args['countryball'][2][-1] != "s":
        plural = "s"
    elif newcount >= 2:
        plural = "es"
    else:
        plural = ""
    
    await ctx.send(f'{ctx.message.author.mention} Completed giving {newcount}{special}{ball_name}{plural} to {parsed_args['user'].mention} ({parsed_args['user'].name})!',file=selfcord.File(f'{name}.json'))
    os.remove(f"{name}.json")

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
        

@bot.event
async def on_command_error(ctx, error):
    print(f'<@{config['your_user_id']}> Command error: `{error}`', file=sys.stderr)  # Print error to stderr

@bot.event
async def on_error(event, *args, **kwargs):
    exc_type, exc_value, exc_tb = sys.exc_info()
    error_message = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print(f'<@{config['your_user_id']}> An error occurred: `{error_message}`', file=sys.stderr)  # Print error to stderr

# bot.run('a')
bot.run(config['tokens']['storage'])
