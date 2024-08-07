#!~/.venvs/3.12/bin/python3.12
import os
from PIL import Image
from keras._tf_keras.keras.models import load_model
import numpy as np
from keras._tf_keras.keras.preprocessing.image import img_to_array
import selfcord
from selfcord.ext import tasks
from discord_webhook import DiscordWebhook
from io import BytesIO
import yaml
import requests
import random
import asyncio

from utils import getconfig
from utils import predict

os.chdir(os.path.dirname(os.path.abspath(__file__)))

config = getconfig.get()


client = selfcord.Client()

@client.event
async def on_ready():
    global servers
    servers = list(config['servers3'])# + list(config['servers2'])
    task1.start()
    print("Running as {0} ({1})!".format(client.user.name, client.user.id))

countryballs = ['British Empire', 'Reichtangle', 'Russian Empire', 'Mongol Empire', 'Kalmar Union', 'Roman Empire', 'Polish-Lithuanian Commonwealth', 'Qin Dynasty', 'German Empire', 'Holy Roman Empire', 'Austria-Hungary', 'Hunnic Empire', 'Japanese Empire', 'Republic of China', 'Soviet Union', 'United States', 'Vatican', 'Russia', 'China', 'Austrian Empire', 'India', 'Ancient Greece', 'Japan', 'Korea', 'Napoleonic France', 'Ottoman Empire', 'Republic of Venice', 'South Korea', 'France', 'Spanish Empire', 'Achaemenid Empire', 'Macedon', 'United Kingdom', 'Pakistan', 'Ancient Egypt', 'Brazil', 'Byzantium', 'Greenland', 'Portuguese Empire', 'Qing', 'British Raj', 'Carthage', 'Italy', 'Kingdom of Italy', 'Egypt', 'Russian Soviet Federative Socialist Republic', 'Turkey', 'French Empire', 'Iran', 'Kingdom of Greece', 'African Union', 'Arab League', 'Kingdom of Hungary', 'Confederate States', 'Gaul', 'Germania', 'Indonesia', 'Mayan Empire', 'Yugoslavia', 'Germany', 'Australia', 'Hong Kong', 'Israel', 'Xiongnu', 'Swedish Empire', 'Spain', 'Antarctica', 'Ming Dynasty', 'Saudi Arabia', 'Franks', 'League of Nations', 'Monaco', 'Union of South Africa', 'Ukraine', 'Canada', 'Poland', 'Kingdom of Brandenburg', 'Sweden', 'Macau', 'Scotland', 'South Africa', 'Greece', 'Vietnam', 'Safavid Empire', 'Thailand', 'Parthian Empire', 'North Korea', 'England', 'European Union', 'Francoist Spain', 'Manchukuo', 'NATO', 'Republican Spain', 'United Arab Republic', 'United Nations', 'Warsaw Pact', 'Weimar Republic', 'Zhou', 'Yuan Dynasty', 'Algeria', 'Argentina', 'Bangladesh', 'Colombia', 'Czechia', 'Iraq', 'Malaysia', 'Mexico', 'Myanmar', 'Netherlands', 'Nigeria', 'Norway', 'Peru', 'Philippines', 'Portugal', 'Prussia', 'Romania', 'Singapore', 'Switzerland', 'Syria', 'Tuvalu', 'UAE', 'Venezuela', 'Mali Empire', 'Ukrainian Soviet Socialist Republic', 'Ancient Athens', 'Ancient Sparta', 'Babylon', 'Czechoslovakia', 'Ethiopian Empire', 'French Indochina', 'Nauru', 'Numidia', 'Quebec', 'Siam', 'South Vietnam', 'Taiwan', 'Wales', 'West Germany', 'Cuba', 'Kingdom of Egypt', 'Mughal Empire', 'Angola', 'Austria', 'Azerbaijan', 'Bahamas', 'Belarus', 'Belgium', 'Bolivia', 'Bulgaria', 'Chile', 'Croatia', 'Cyprus', 'DR Congo', 'Denmark', 'Ecuador', 'Ethiopia', 'Finland', 'Hungary', 'Jordan', 'Kazakhstan', 'Kenya', 'Kuwait', 'Libya', 'Morocco', 'North Vietnam', 'Oman', 'Qatar', 'San Marino', 'Serbia', 'Slovakia', 'Sri Lanka', 'Sudan', 'Tunisia', 'Turkmenistan', 'Uzbekistan', 'Yemen', 'Iberian Union', 'Faroe Islands', 'Trinidad and Tobago', 'East Germany', 'Free France', 'Jamaica', 'Maldives', 'Northern Ireland', 'Tibet', 'Golden Horde', 'Vichy France', 'Andorra', 'Brunei', 'Byelorussian Soviet Socialist Republic', 'Micronesia', 'Tonga', 'Grand Duchy of Tuscany', 'Khedivate of Egypt', 'Khmer Empire', 'Barbados', 'Marshall Islands', 'Armenia', 'Bahrain', 'Cambodia', 'Chad', 'Equatorial Guinea', 'Congo Free State', 'Georgia', 'Ghana', 'Guatemala', 'Guyana', 'Ireland', 'Kyrgyzstan', 'Latvia', 'Lithuania', 'Mali', 'Malta', 'Fatimid Caliphate', 'Mongolia', 'New Zealand', 'Samoa', 'Slovenia', 'Togo', 'Uganda', 'Uruguay', 'Zambia', 'Zimbabwe', 'Malawi', 'Kingdom of Sardinia', 'Costa Rica', 'Dominica', 'Guinea-Bissau', 'Sao Tome and Principe', 'Tannu Tuva', 'Seychelles', 'Afghanistan', 'Albania', 'Belize', 'Bosnia and Herzegovina', 'Botswana', 'Cameroon', 'Ceylon', 'Congo', "Cote d'Ivoire", 'Dominican Republic', 'Eritrea', 'Estonia', 'Eswatini', 'Fiji', 'Free City of Danzig', 'Gambia', 'Haiti', 'Honduras', 'Khiva', 'Laos', 'Lebanon', 'Liechtenstein', 'Moldova', 'Mozambique', 'Nepal', 'Nicaragua', 'Niger', 'Palestine', 'Paraguay', 'Saint Kitts and Nevis', 'Saint Lucia', 'Somaliland', 'South Sudan', 'South Yemen', 'Tajikistan', 'Tanzania', 'Western Sahara', 'Cape Verde', 'Guinea', 'Grenada', 'Palau', 'St. Vincent and the Grenadines', 'Solomon Islands', 'Vanuatu', 'Principality of Moldavia', 'Qajar Dynasty', 'Antigua and Barbuda', 'Benin', 'Majapahit', 'Bhutan', 'Burkina Faso', 'Nanda Empire', 'Burundi', 'Central African Republic', 'Comoros', 'El Salvador', 'Gabon', 'Hejaz', 'Iceland', 'Kiribati', 'Kosovo', 'Lesotho', 'Liberia', 'Luxembourg', 'Madagascar', 'Mauritania', 'Mauritius', 'Montenegro', 'Namibia', 'North Macedonia', 'Panama', 'Papua New Guinea', 'Paris Commune', 'Rwanda', 'Senegal', 'Sierra Leone', 'Somalia', 'Suriname', 'Timor-Leste', 'Djibouti']
sorted = countryballs.copy()
sorted.sort()

catchball = []
webhookurl = 'https://discord.com/api/webhooks/1268374793040695316/2trCno1syYd4r2l9uUXlCT3MqGF4BS9Rl0s9_TwEZ8zlOxnxCUMIvOUBOsHqTDV8tfya'
ballsdex_userid = 999736048596816014
with open('rarity.txt','r+') as f:
    raritylist = f.readlines()

@tasks.loop(minutes=0.5)
async def task1():
    global servers
    for serverid in servers:
        try:
            guild = client.get_guild(serverid)
            channel = guild.text_channels[0]
            print(guild.name,channel.name)
            await channel.send(random.randint(1,1000))
            await asyncio.sleep(2)
        except Exception as e:
            print()
            print(client.get_guild(serverid).name)
            print(e)
            print()


    


@client.event
async def on_message(message: selfcord.Message):
    global catchball
    
    if message.author.id == ballsdex_userid:
        if message.content == 'A wild countryball appeared!':
            img_url = message.attachments[0].url
            ball = predict.makePrediction(img_url)
            catchball.append(ball)
            await message.channel.send(ball)
            interaction = await message.components[0].children[0].click()
        

        elif f'<@{client.user.id}> You caught' in message.content:
            mention = f'<@{config["your_user_id"]}>'

            #get stats
            stats = message.content.split('`(',1)[1].split(')`',1)[0]

            #get ball
            ball = message.content.split('You caught **',1)[1].split('!',1)[0]

            #get special
            special = ''
            if 'mythical aura' in message.content:
                special = f' (MYTHICAL) {mention}'
            if 'shiny countryball' in message.content:
                special = f' (SHINY) {mention}'
            
            #get rarity
            for rare in raritylist:
                temp = rare.split('. ',1)
                ballrarity = temp[0]
                ballname = temp[1].replace('\n','')
                if ball == ballname:
                    rarity = ballrarity
                    break

            #send message in console
            printmsg = f'Caught {ball} `({stats})`{special}'
            print(printmsg)
            
            #send give command
            give_user = client.get_user(1268896529351966771)
            give_guild = message.guild
            give_channel = selfcord.utils.get(give_guild.channels, name='general')
            hexid = stats.split(', ')[0]
            if hexid[0] == '#':
                hexid = hexid[1:]
            commands = [command async for command in give_channel.slash_commands()]
            print(give_user.name,give_guild.name)
            # print(commands)
            y = False
            for command in commands:
                print(command.name)
                x = False
                if command.name == 'balls':
                    y = True
                    print('balls found')
                    for subcommand in command.children:
                        print(subcommand.name)
                        if subcommand.name == 'give':
                            print('sending')
                            give = await subcommand.__call__(channel=give_channel, user=give_user, countryball=int(hexid, 16))
                            print('sent?')
                            x = True
                            break
                    if not x:
                        print('not found!>?!>')
                    else:
                        break
            if not y:
                print('not y')

            #get emoji
            emoji = ''
            await asyncio.sleep(5)
            print(give.name)
            print(give.nonce)
            print(give.type)
            print(give.successful)
            print(give.message)
            print(type(give))
            # await asyncio.sleep(10)
            # print(type(give))
            if type(give) == selfcord.interactions.Interaction:
                give_text = give.message.content
                emoji = '<'+give_text.split('<',1)[1].split('>',1)[0]+'>'
            else:
                print('nope')
            
            
            #send message in webhook
            catchmsg = f'Caught {emoji} {rarity}. {ball} `({stats})`{special} {message.jump_url}'
            webhook = DiscordWebhook(url=webhookurl, content=catchmsg)
            response = webhook.execute()

        elif message.content == f'<@{client.user.id}> Wrong name!':
            printmsg = 'Wrong name!'
            print(printmsg)

            mention = f'<@{config["your_user_id"]}>'
            catchmsg = f'Wrong name! {mention} {message.jump_url}'
            webhook = DiscordWebhook(url=webhookurl, content=catchmsg)
            response = webhook.execute()

@client.event
async def on_modal(modal: selfcord.Modal):
    global catchball
    modal.components[0].children[0].answer(catchball[-1])
    await modal.submit()


client.run(config['tokens']['catch2'])