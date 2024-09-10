#!~/.venvs/3.12/bin/python3.12
import os
import selfcord
import sys
import requests
import traceback

from utils import getconfig
from utils import webhooks

os.chdir(os.path.dirname(os.path.abspath(__file__)))

config = getconfig.get()

error_handler = webhooks.makeObject(config['urls']['allservers'],os.path.basename(__file__))

# Redirect stderr to the webhook handler
sys.stderr = error_handler

servers = {
    'pizzahut0667':[
        1268358108942696481,
        1268358043846971393,
        1268357963148558480,
        1268354445310164992,
        1268356884012859433,
        1270517020458487808,
        1270517247747559465,
        1270517706319466547,
        1269092722799546378,
        1269092673797488640,
        1269092641497419887,
        1269092599059189812,
        1269092543933710449,
        1270567971126906900,
        1270568006761578546,
        1270568043453616138
    ],
    'eddy2.0sadly':[
        1270613345548111974,
        1270613241839751190,
        1270613120745734216,
        1270613086239461447,
        1270613049463803928,
        1270612946116018260,
        1270612918085353566,
        1270612785704865874,
        1271985229275467938,
        1271985198808043633,
        1271984602524684409,
        1271984571474247750,
        1271984642215383133,
        1271984768958992497,
        1271984830443159664,
        1271984992611995729
    ],
    'cheesecakefactory66580':[
        1272348245992931501,
        1272348146688851998,
        1272348731471298601,
        1272348759279276115,
        1272348793681088633,
        1272348943128330241,
        1272348903299350609,
        1272349044626165801,
        1272365119619334194,
        1272365089403703411,
        1272365151353442414,
        1272365315749052517,
        1272365344006340650,
        1272365373684977734,
        1272365401334091816,
        1272365433793675335
    ],
    'charliebrownbitches':[
        1272622218127610049,
        1272622260930220164,
        1272622342836719666,
        1272622387799523338,
        1272622414580416624,
        1272622464039387256,
        1272622499351494738,
        1272622523850424380,
        1272609682359455817,
        1272609805952880783,
        1272609652667846764,
        1272609561752113225,
        1272609614269251705,
        1272609530173460644,
        1272609501693874237,
        1272609469205057607
    ],
    'justaown1':[
        1268358108942696481,
        1268358043846971393,
        1268357963148558480,
        1268354445310164992,
        1268356884012859433,
        1270517020458487808,
        1270517247747559465,
        1270517706319466547
    ],
    'allisaslaysforevs':[
        1269092722799546378,
        1269092673797488640,
        1269092641497419887,
        1269092599059189812,
        1269092543933710449,
        1270567971126906900,
        1270568006761578546,
        1270568043453616138
    ],
    'abwin3':[
        1270613345548111974,
        1270613241839751190,
        1270613120745734216,
        1270613086239461447,
        1270613049463803928,
        1270612946116018260,
        1270612918085353566,
        1270612785704865874
    ],
    'iforgorcuzyes':[
        1271985229275467938,
        1271985198808043633,
        1271984602524684409,
        1271984571474247750,
        1271984642215383133,
        1271984768958992497,
        1271984830443159664,
        1271984992611995729
    ],
    'papajohns6658':[
        1272348245992931501,
        1272348146688851998,
        1272348731471298601,
        1272348759279276115,
        1272348793681088633,
        1272348943128330241,
        1272348903299350609,
        1272349044626165801
    ],
    'littleceaser0667':[
        1272365119619334194,
        1272365089403703411,
        1272365151353442414,
        1272365315749052517,
        1272365344006340650,
        1272365373684977734,
        1272365401334091816,
        1272365433793675335
    ],
    'chipotlebowlsolos':[
        1272622218127610049,
        1272622260930220164,
        1272622342836719666,
        1272622387799523338,
        1272622414580416624,
        1272622464039387256,
        1272622499351494738,
        1272622523850424380
    ],
    'olivegardenbreadstick_.':[
        1272609682359455817,
        1272609805952880783,
        1272609652667846764,
        1272609561752113225,
        1272609614269251705,
        1272609530173460644,
        1272609501693874237,
        1272609469205057607
    ]
}

roles = {
    'allservers':'proficour2',
    'storage':'justastorage',
    'catch':{
        '1':'pizzahut0667',
        '2':'eddy2.0sadly',
        '3':'cheesecakefactory66580',
        '4':'charliebrownbitches'
    },
    'own':{
        '1':'justaown1',
        '2':'allisaslaysforevs',
        '3':'abwin3',
        '4':'iforgorcuzyes',
        '5':'papajohns6658',
        '6':'littleceaser0667',
        '7':'chipotlebowlsolos',
        '8':'olivegardenbreadstick_.'
    }
}

users = {
    'proficour2':1268101370997641291,
    'justastorage':1273823384278532128,
    'pizzahut0667':1266938888119910500,
    'eddy2.0sadly':1272676930658762844,
    'cheesecakefactory66580':1272368267184574495,
    'charliebrownbitches':1272610773012844679,
    'justaown1':1273850668725043251,
    'allisaslaysforevs':1249390531977547880,
    'abwin3':1077104788908560384,
    'iforgorcuzyes':1271972537064231095,
    'papajohns6658':1272211028981190688,
    'littleceaser0667':1272227666803687548,
    'chipotlebowlsolos':1272616894431756352,
    'olivegardenbreadstick_.':1272607892897267736
}

config = getconfig.get()

client = selfcord.Client()



@client.event
async def on_ready():
    print("Running as {0} ({1})!".format(client.user.name, client.user.id))

@client.event
async def on_message(message: selfcord.Message):
    # if message.author.id == 1273823384278532128: #storage account
        # if message.channel.id == 1281843539369529505: #storage account dms
            if message.content.startswith('.status'):
                offline = []
                storage_channel = await client.fetch_channel(1281843539369529505)
                await storage_channel.send('ping')
                for guild in client.guilds:
                    if guild.id != 1254513690976325742: #farm server with the boys
                        required_users = []
                        for user in list(servers.keys()):
                            for server in servers[user]:
                                if guild.id == server:
                                    required_users.append(user)
                        
                        for c in guild.channels:
                            if c.name == 'general':
                                channel = c
                                break

                        messages = [msg async for msg in channel.history(limit=10)]
                        
                        for msg in messages:
                            if len(required_users) == 0:
                                break
                            for required_user in required_users:
                                if msg.author.id == users[required_user]:
                                    required_users.remove(required_user)
                        # print(required_users)
                        offline = offline + required_users
                storage_online = False
                messages = [msg async for msg in storage_channel.history(limit=10)]
                for msg in messages:
                    print(msg.content)
                    print(msg.author.id)
                    if msg.content == 'pong' and msg.author.id == 1273823384278532128:
                        storage_online = True
                        break
                if not storage_online:
                    offline.append(roles['storage'])

                offline = list(set(offline))
                online = list(users.keys())
                print(list(users.keys()))
                print(offline)
                for user in online:
                    if user in offline:
                        online.remove(user)
                status = {}
                for user in online:
                    status[user] = 'online'
                for user in offline:
                    status[user] = 'offline'
                emojidict = {
                    'online':'✅',
                    'offline':'❌'
                }
                sendmsg = f'''## Status for each account:
{emojidict[status[roles['allservers']]]} - `allservers` - <@{users[roles['allservers']]}>
{emojidict[status[roles['storage']]]} - `storage` - <@{users[roles['storage']]}>
{emojidict[status[roles['catch']['1']]]} - `catch 1` - <@{users[roles['catch']['1']]}>
{emojidict[status[roles['catch']['2']]]} - `catch 2` - <@{users[roles['catch']['2']]}>
{emojidict[status[roles['catch']['3']]]} - `catch 3` - <@{users[roles['catch']['3']]}>
{emojidict[status[roles['catch']['4']]]} - `catch 4` - <@{users[roles['catch']['4']]}>
{emojidict[status[roles['own']['1']]]} - `own 1` - <@{users[roles['own']['1']]}>
{emojidict[status[roles['own']['2']]]} - `own 2` - <@{users[roles['own']['2']]}>
{emojidict[status[roles['own']['3']]]} - `own 3` - <@{users[roles['own']['3']]}>
{emojidict[status[roles['own']['4']]]} - `own 4` - <@{users[roles['own']['4']]}>
{emojidict[status[roles['own']['5']]]} - `own 5` - <@{users[roles['own']['5']]}>
{emojidict[status[roles['own']['6']]]} - `own 6` - <@{users[roles['own']['6']]}>
{emojidict[status[roles['own']['7']]]} - `own 7` - <@{users[roles['own']['7']]}>
{emojidict[status[roles['own']['8']]]} - `own 8` - <@{users[roles['own']['8']]}>
'''
                # print(sendmsg)
                await message.channel.send(sendmsg)

                        



@client.event
async def on_command_error(ctx, error):
    print(f'<@{config['your_user_id']}> Command error: `{error}`', file=sys.stderr)  # Print error to stderr

@client.event
async def on_error(event, *args, **kwargs):
    exc_type, exc_value, exc_tb = sys.exc_info()
    error_message = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print(f'<@{config['your_user_id']}> An error occurred: `{error_message}`', file=sys.stderr)  # Print error to stderr

client.run(config['tokens']['test'])