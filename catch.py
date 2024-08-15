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

os.chdir(os.path.dirname(os.path.abspath(__file__)))


config = getconfig.get()

model = load_model('model.keras')
image_size = (128, 128)

countryballs = ['British Empire', 'Reichtangle', 'Russian Empire', 'Mongol Empire', 'Kalmar Union', 'Roman Empire', 'Polish-Lithuanian Commonwealth', 'Qin Dynasty', 'German Empire', 'Holy Roman Empire', 'Austria-Hungary', 'Hunnic Empire', 'Japanese Empire', 'Republic of China', 'Soviet Union', 'United States', 'Vatican', 'Russia', 'China', 'Austrian Empire', 'India', 'Ancient Greece', 'Japan', 'Korea', 'Napoleonic France', 'Ottoman Empire', 'Republic of Venice', 'South Korea', 'France', 'Spanish Empire', 'Achaemenid Empire', 'Macedon', 'United Kingdom', 'Pakistan', 'Ancient Egypt', 'Brazil', 'Byzantium', 'Greenland', 'Portuguese Empire', 'Qing', 'British Raj', 'Carthage', 'Italy', 'Kingdom of Italy', 'Egypt', 'Russian Soviet Federative Socialist Republic', 'Turkey', 'French Empire', 'Iran', 'Kingdom of Greece', 'African Union', 'Arab League', 'Kingdom of Hungary', 'Confederate States', 'Gaul', 'Germania', 'Indonesia', 'Mayan Empire', 'Yugoslavia', 'Germany', 'Australia', 'Hong Kong', 'Israel', 'Xiongnu', 'Swedish Empire', 'Spain', 'Antarctica', 'Ming Dynasty', 'Saudi Arabia', 'Franks', 'League of Nations', 'Monaco', 'Union of South Africa', 'Ukraine', 'Canada', 'Poland', 'Kingdom of Brandenburg', 'Sweden', 'Macau', 'Scotland', 'South Africa', 'Greece', 'Vietnam', 'Safavid Empire', 'Thailand', 'Parthian Empire', 'North Korea', 'England', 'European Union', 'Francoist Spain', 'Manchukuo', 'NATO', 'Republican Spain', 'United Arab Republic', 'United Nations', 'Warsaw Pact', 'Weimar Republic', 'Zhou', 'Yuan Dynasty', 'Algeria', 'Argentina', 'Bangladesh', 'Colombia', 'Czechia', 'Iraq', 'Malaysia', 'Mexico', 'Myanmar', 'Netherlands', 'Nigeria', 'Norway', 'Peru', 'Philippines', 'Portugal', 'Prussia', 'Romania', 'Singapore', 'Switzerland', 'Syria', 'Tuvalu', 'UAE', 'Venezuela', 'Mali Empire', 'Ukrainian Soviet Socialist Republic', 'Ancient Athens', 'Ancient Sparta', 'Babylon', 'Czechoslovakia', 'Ethiopian Empire', 'French Indochina', 'Nauru', 'Numidia', 'Quebec', 'Siam', 'South Vietnam', 'Taiwan', 'Wales', 'West Germany', 'Cuba', 'Kingdom of Egypt', 'Mughal Empire', 'Angola', 'Austria', 'Azerbaijan', 'Bahamas', 'Belarus', 'Belgium', 'Bolivia', 'Bulgaria', 'Chile', 'Croatia', 'Cyprus', 'DR Congo', 'Denmark', 'Ecuador', 'Ethiopia', 'Finland', 'Hungary', 'Jordan', 'Kazakhstan', 'Kenya', 'Kuwait', 'Libya', 'Morocco', 'North Vietnam', 'Oman', 'Qatar', 'San Marino', 'Serbia', 'Slovakia', 'Sri Lanka', 'Sudan', 'Tunisia', 'Turkmenistan', 'Uzbekistan', 'Yemen', 'Iberian Union', 'Faroe Islands', 'Trinidad and Tobago', 'East Germany', 'Free France', 'Jamaica', 'Maldives', 'Northern Ireland', 'Tibet', 'Golden Horde', 'Vichy France', 'Andorra', 'Brunei', 'Byelorussian Soviet Socialist Republic', 'Micronesia', 'Tonga', 'Grand Duchy of Tuscany', 'Khedivate of Egypt', 'Khmer Empire', 'Barbados', 'Marshall Islands', 'Armenia', 'Bahrain', 'Cambodia', 'Chad', 'Equatorial Guinea', 'Congo Free State', 'Georgia', 'Ghana', 'Guatemala', 'Guyana', 'Ireland', 'Kyrgyzstan', 'Latvia', 'Lithuania', 'Mali', 'Malta', 'Fatimid Caliphate', 'Mongolia', 'New Zealand', 'Samoa', 'Slovenia', 'Togo', 'Uganda', 'Uruguay', 'Zambia', 'Zimbabwe', 'Malawi', 'Kingdom of Sardinia', 'Costa Rica', 'Dominica', 'Guinea-Bissau', 'Sao Tome and Principe', 'Tannu Tuva', 'Seychelles', 'Afghanistan', 'Albania', 'Belize', 'Bosnia and Herzegovina', 'Botswana', 'Cameroon', 'Ceylon', 'Congo', "Cote d'Ivoire", 'Dominican Republic', 'Eritrea', 'Estonia', 'Eswatini', 'Fiji', 'Free City of Danzig', 'Gambia', 'Haiti', 'Honduras', 'Khiva', 'Laos', 'Lebanon', 'Liechtenstein', 'Moldova', 'Mozambique', 'Nepal', 'Nicaragua', 'Niger', 'Palestine', 'Paraguay', 'Saint Kitts and Nevis', 'Saint Lucia', 'Somaliland', 'South Sudan', 'South Yemen', 'Tajikistan', 'Tanzania', 'Western Sahara', 'Cape Verde', 'Guinea', 'Grenada', 'Palau', 'St. Vincent and the Grenadines', 'Solomon Islands', 'Vanuatu', 'Principality of Moldavia', 'Qajar Dynasty', 'Antigua and Barbuda', 'Benin', 'Majapahit', 'Bhutan', 'Burkina Faso', 'Nanda Empire', 'Burundi', 'Central African Republic', 'Comoros', 'El Salvador', 'Gabon', 'Hejaz', 'Iceland', 'Kiribati', 'Kosovo', 'Lesotho', 'Liberia', 'Luxembourg', 'Madagascar', 'Mauritania', 'Mauritius', 'Montenegro', 'Namibia', 'North Macedonia', 'Panama', 'Papua New Guinea', 'Paris Commune', 'Rwanda', 'Senegal', 'Sierra Leone', 'Somalia', 'Suriname', 'Timor-Leste', 'Djibouti']
sorted = countryballs.copy()
sorted.sort()

catchball = []
wrongs = {}

all_catches = config['all_catches_webhook_url']
rare_catches = config['rare_catches_webhook_url']

ballsdex_userid = 999736048596816014

with open('rarity.txt','r+') as f:
    raritylist = f.readlines()


def makePrediction(img_url):
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content)).convert('RGB')

    img = img.resize(image_size)
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions, axis=1)
    return sorted[list(predicted_class)[0]]

client = selfcord.Client()

@client.event
async def on_ready():
    global servers
    servers = list(config['servers1']) + list(config['servers2'])
    task1.start()
    print("Running as {0} ({1})!".format(client.user.name, client.user.id))

@tasks.loop(minutes=0.5)
async def task1():
    global servers
    for serverid in servers:
        try:
            guild = client.get_guild(serverid)
            if guild is None:
                guild = await client.fetch_guild(serverid)
            channel = guild.text_channels[0]
            print(guild.name,channel.name)
            await channel.send(random.randint(1,1000))
            await asyncio.sleep(2)
        except Exception as e:
            print()
            print(e)
            print()

@client.event
async def on_message(message: selfcord.Message):
    global catchball
    global wrongs
    
    if message.author.id == ballsdex_userid:
        if message.content == 'A wild countryball appeared!':
            img_url = message.attachments[0].url
            ball = makePrediction(img_url)
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
                special = f' (:milky_way: **MYTHICAL** :milky_way:) {mention}'
            if 'shiny countryball' in message.content:
                special = f' (:sparkles: **SHINY** :sparkles:) {mention}'
            
            #get rarity
            for rare in raritylist:
                temp = rare.split('. ',2)
                ballrarity = temp[0]
                ballname = temp[2].replace('\n','')
                if ball == ballname:
                    rarity = ballrarity
                    break

            #send message in console
            printmsg = f'Caught {ball} `({stats})`{special}'
            print(printmsg)
            
            #get usre and channel
            give_user = client.get_user(1268896529351966771)
            if give_user is None:
                give_user = await client.fetch_user(1268896529351966771)
            give_guild = message.guild
            give_channel = selfcord.utils.get(give_guild.channels, name='general')
            if give_channel is None:
                give_channel = message.channel

            #get hexid
            hexid = stats.split(', ')[0]
            if hexid[0] == '#':
                hexid = hexid[1:]
            
            #get commands and send give command
            commands = [command async for command in give_channel.slash_commands()]
            for command in commands:
                if command.name == 'balls':
                    for subcommand in command.children:
                        print(subcommand.name)
                        if subcommand.name == 'give':
                            give = await subcommand.__call__(channel=give_channel, user=give_user, countryball=int(hexid, 16))
                            break
                    break

            #get emoji
            emoji = ''
            await asyncio.sleep(5)
            if type(give) == selfcord.interactions.Interaction:
                give_text = give.message.content
                emoji = '<'+give_text.split('<',1)[1].split('>',1)[0]+'>'
            else:
                emoji = '<emoji not found>'
            
            catchmsg = f'Caught {emoji} {rarity}. {ball} `({stats})`{special} {message.jump_url}'

            #send message in all catches webhook
            webhook = DiscordWebhook(url=all_catches, content=catchmsg)
            response = webhook.execute()

            #send message in rare catches webhook
            if int(rarity) <= 11 or special != '':
                webhook = DiscordWebhook(url=rare_catches, content=catchmsg)
                response = webhook.execute()


        elif message.content == f'<@{client.user.id}> Wrong name!':
            reference = await message.channel.fetch_message(message.reference.message_id)

            if reference.id in wrongs:
                wrongs[reference.id] += 1
            else:
                wrongs[reference.id] = 1
            print(wrongs[reference.id])
            if wrongs[reference.id] == 4:
                mention = f'<@{config["your_user_id"]}>'
                catchmsg = f'Wrong name after 4 attempts! {mention} {message.jump_url}'
                webhook = DiscordWebhook(url=all_catches, content=catchmsg)
                response = webhook.execute()
            else:
                await asyncio.sleep(4)
                img_url = message.attachments[0].url
                ball = makePrediction(img_url)
                catchball.append(ball)
                interaction = await reference.components[0].children[0].click()





@client.event
async def on_message_edit(before: selfcord.Message, message: selfcord.Message):
    global wrongs

    if message.author.id == ballsdex_userid:

        if f'<@{client.user.id}> You caught' in message.content:
            mention = f'<@{config["your_user_id"]}>'

            #get stats
            stats = message.content.split('`(',1)[1].split(')`',1)[0]

            #get ball
            ball = message.content.split('You caught **',1)[1].split('!',1)[0]

            #get special
            special = ''
            if 'mythical aura' in message.content:
                special = f' (:milky_way: **MYTHICAL** :milky_way:) {mention}'
            if 'shiny countryball' in message.content:
                special = f' (:sparkles: **SHINY** :sparkles:) {mention}'
            
            #get rarity
            for rare in raritylist:
                temp = rare.split('. ',2)
                ballrarity = temp[0]
                ballname = temp[2].replace('\n','')
                if ball == ballname:
                    rarity = ballrarity
                    break

            #send message in console
            printmsg = f'Caught {ball} `({stats})`{special}'
            print(printmsg)
            
            #get usre and channel
            give_user = client.get_user(1268896529351966771)
            if give_user is None:
                give_user = await client.fetch_user(1268896529351966771)
            give_guild = message.guild
            give_channel = selfcord.utils.get(give_guild.channels, name='general')
            if give_channel is None:
                give_channel = message.channel

            #get hexid
            hexid = stats.split(', ')[0]
            if hexid[0] == '#':
                hexid = hexid[1:]
            
            #get commands and send give command
            commands = [command async for command in give_channel.slash_commands()]
            for command in commands:
                if command.name == 'balls':
                    for subcommand in command.children:
                        print(subcommand.name)
                        if subcommand.name == 'give':
                            give = await subcommand.__call__(channel=give_channel, user=give_user, countryball=int(hexid, 16))
                            break
                    break

            #get emoji
            emoji = ''
            await asyncio.sleep(5)
            if type(give) == selfcord.interactions.Interaction:
                give_text = give.message.content
                emoji = '<'+give_text.split('<',1)[1].split('>',1)[0]+'>'
            else:
                emoji = '<emoji not found>'
            
            catchmsg = f'Caught {emoji} {rarity}. {ball} `({stats})`{special} {message.jump_url}'

            #send message in all catches webhook
            webhook = DiscordWebhook(url=all_catches, content=catchmsg)
            response = webhook.execute()

            #send message in rare catches webhook
            if int(rarity) <= 11 or special != '':
                webhook = DiscordWebhook(url=rare_catches, content=catchmsg)
                response = webhook.execute()


        elif message.content == f'<@{client.user.id}> Wrong name!':
            reference = await message.channel.fetch_message(message.reference.message_id)

            if reference.id in wrongs:
                wrongs[reference.id] += 1
            else:
                wrongs[reference.id] = 1
            print(wrongs[reference.id])
            if wrongs[reference.id] == 4:
                mention = f'<@{config["your_user_id"]}>'
                catchmsg = f'Wrong name after 4 attempts! {mention} {message.jump_url}'
                webhook = DiscordWebhook(url=all_catches, content=catchmsg)
                response = webhook.execute()
            else:
                await asyncio.sleep(4)
                img_url = message.attachments[0].url
                ball = makePrediction(img_url)
                catchball.append(ball)
                interaction = await reference.components[0].children[0].click()

@client.event
async def on_modal(modal: selfcord.Modal):
    global catchball
    modal.components[0].children[0].answer(catchball[-1])
    await modal.submit()


client.run(config['tokens']['catch'])