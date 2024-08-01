from discum.utils.slash import SlashCommander
import discum
import os
from PIL import Image
from keras._tf_keras.keras.models import load_model
import numpy as np
from keras._tf_keras.keras.preprocessing import image
from keras._tf_keras.keras.preprocessing.image import img_to_array
import selfcord
from selfcord.ext import tasks
from discord_webhook import DiscordWebhook
from io import BytesIO
import os
import yaml
import requests
import random
import asyncio

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def getconfig():
    if not os.path.isfile('config.yml'):
        with open('config.yml','x+') as file:
            file.write('''---

# BOT CONFIG
bot:
  # selfcord bot token
  token: 

  # The command prefix for the bot
  command_prefix: 

''')
        print('\nA config file (config.yml) has been generated. Please fill out the values in the file and run bot.py again.\n')
        quit()
        exit()
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)
    return config
config = getconfig()

if not os.path.isfile('model.keras'):
    print('downloading model file...')
    r = requests.get('https://files.catbox.moe/0yjdn8.keras')
    with open('model.keras','x+') as file:
        file.write(r.content)
    print('downloaded model file!')

model = load_model('model.keras')
image_size = (128, 128)
def predict_category(img_url):
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content)).convert('RGB')

    img = img.resize(image_size)
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions, axis=1)
    
    return os.listdir('database/')[list(predicted_class)[0]]


client = selfcord.Client()
client2 = discum.Client(token=config['bot']['token'], log=False)

@client.event
async def on_ready():
    task1.start()
    print("Running as {0} ({1})!".format(client.user.name, client.user.id))

total = 5

countryballs = []
string = '''1. British Empire
1. Reichtangle
1. Russian Empire
4. Mongol Empire
5. Kalmar Union
5. Roman Empire
7. Polish-Lithuanian Commonwealth
8. Qin Dynasty
9. German Empire
10. Holy Roman Empire
11. Austria-Hungary
11. Hunnic Empire
11. Japanese Empire
11. Republic of China
11. Soviet Union
11. United States
17. Vatican
18. Russia
19. China
20. Austrian Empire
21. India
22. Ancient Greece
22. Japan
22. Korea
22. Napoleonic France
22. Ottoman Empire
27. Republic of Venice
27. South Korea
29. France
29. Spanish Empire
31. Achaemenid Empire
31. Macedon
31. United Kingdom
34. Pakistan
35. Ancient Egypt
35. Brazil
35. Byzantium
35. Greenland
35. Portuguese Empire
35. Qing
41. British Raj
41. Carthage
41. Italy
41. Kingdom of Italy
45. Egypt
45. Russian Soviet Federative Socialist Republic
47. Turkey
48. French Empire
49. Iran
49. Kingdom of Greece
51. African Union
51. Arab League
51. Kingdom of Hungary
51. Confederate States
51. Gaul
51. Germania
51. Indonesia
51. Mayan Empire
51. Yugoslavia
60. Germany
61. Australia
61. Hong Kong
61. Israel
61. Xiongnu
65. Swedish Empire
66. Spain
67. Antarctica
67. Ming Dynasty
67. Saudi Arabia
70. Franks
70. League of Nations
70. Monaco
70. Union of South Africa
74. Ukraine
75. Canada
76. Poland
76. Kingdom of Brandenburg
78. Sweden
79. Macau
79. Scotland
79. South Africa
82. Greece
83. Vietnam
84. Safavid Empire
85. Thailand
85. Parthian Empire
87. North Korea
88. England
88. European Union
88. Francoist Spain
88. Manchukuo
88. NATO
88. Republican Spain
88. United Arab Republic
88. United Nations
88. Warsaw Pact
88. Weimar Republic
88. Zhou
99. Yuan Dynasty
100. Algeria
100. Argentina
100. Bangladesh
100. Colombia
100. Czechia
100. Iraq
100. Malaysia
100. Mexico
100. Myanmar
100. Netherlands
100. Nigeria
100. Norway
112. Peru
112. Philippines
112. Portugal
112. Prussia
112. Romania
112. Singapore
112. Switzerland
112. Syria
112. Tuvalu
112. UAE
112. Venezuela
123. Mali Empire
124. Ukrainian Soviet Socialist Republic
125. Ancient Athens
125. Ancient Sparta
125. Babylon
125. Czechoslovakia
125. Ethiopian Empire
125. French Indochina
125. Nauru
125. Numidia
125. Quebec
125. Siam
125. South Vietnam
125. Taiwan
125. Wales
125. West Germany
139. Cuba
140. Kingdom of Egypt
141. Mughal Empire
142. Angola
142. Austria
142. Azerbaijan
142. Bahamas
142. Belarus
142. Belgium
142. Bolivia
142. Bulgaria
142. Chile
142. Croatia
142. Cyprus
142. DR Congo
142. Denmark
142. Ecuador
142. Ethiopia
142. Finland
142. Hungary
142. Jordan
142. Kazakhstan
142. Kenya
142. Kuwait
142. Libya
142. Morocco
142. North Vietnam
142. Oman
142. Qatar
142. San Marino
142. Serbia
142. Slovakia
142. Sri Lanka
142. Sudan
142. Tunisia
142. Turkmenistan
142. Uzbekistan
142. Yemen
142. Iberian Union
178. Faroe Islands
178. Trinidad and Tobago
180. East Germany
180. Free France
180. Jamaica
180. Maldives
180. Northern Ireland
180. Tibet
180. Golden Horde
180. Vichy France
188. Andorra
188. Brunei
188. Byelorussian Soviet Socialist Republic
188. Micronesia
188. Tonga
188. Grand Duchy of Tuscany
188. Khedivate of Egypt
195. Khmer Empire
196. Barbados
196. Marshall Islands
198. Armenia
198. Bahrain
198. Cambodia
198. Chad
198. Equatorial Guinea
198. Congo Free State
198. Georgia
198. Ghana
198. Guatemala
198. Guyana
198. Ireland
198. Kyrgyzstan
198. Latvia
198. Lithuania
198. Mali
198. Malta
198. Fatimid Caliphate
198. Mongolia
198. New Zealand
198. Samoa
198. Slovenia
198. Togo
198. Uganda
198. Uruguay
198. Zambia
198. Zimbabwe
224. Malawi
225. Kingdom of Sardinia
226. Costa Rica
226. Dominica
226. Guinea-Bissau
226. Sao Tome and Principe
226. Tannu Tuva
231. Seychelles
232. Afghanistan
232. Albania
232. Belize
232. Bosnia and Herzegovina
232. Botswana
232. Cameroon
232. Ceylon
232. Congo
232. Cote d'Ivoire
232. Dominican Republic
232. Eritrea
232. Estonia
232. Eswatini
232. Fiji
232. Free City of Danzig
232. Gambia
232. Haiti
232. Honduras
232. Khiva
232. Laos
232. Lebanon
232. Liechtenstein
232. Moldova
232. Mozambique
232. Nepal
232. Nicaragua
232. Niger
232. Palestine
232. Paraguay
232. Saint Kitts and Nevis
232. Saint Lucia
232. Somaliland
232. South Sudan
232. South Yemen
232. Tajikistan
232. Tanzania
232. Western Sahara
269. Cape Verde
269. Guinea
269. Grenada
269. Palau
269. St. Vincent and the Grenadines
269. Solomon Islands
269. Vanuatu
276. Principality of Moldavia
277. Qajar Dynasty
278. Antigua and Barbuda
278. Benin
278. Majapahit
278. Bhutan
278. Burkina Faso
278. Nanda Empire
278. Burundi
278. Central African Republic
278. Comoros
278. El Salvador
278. Gabon
278. Hejaz
278. Iceland
278. Kiribati
278. Kosovo
278. Lesotho
278. Liberia
278. Luxembourg
278. Madagascar
278. Mauritania
278. Mauritius
278. Montenegro
278. Namibia
278. North Macedonia
278. Panama
278. Papua New Guinea
278. Paris Commune
278. Rwanda
278. Senegal
278. Sierra Leone
278. Somalia
278. Suriname
278. Timor-Leste
311. Djibouti'''

countryballs = string.split('\n')
countryballs = [country.split('.')[1] for country in countryballs]

catchball = []
webhookurl = 'https://discord.com/api/webhooks/1268374793040695316/2trCno1syYd4r2l9uUXlCT3MqGF4BS9Rl0s9_TwEZ8zlOxnxCUMIvOUBOsHqTDV8tfya'

serveridlist = [1268358108942696481,1268358043846971393,1268357963148558480]


@tasks.loop(minutes=1)
async def task1():
    for serverid in serveridlist:
        await asyncio.sleep(2)
        guild = client.get_guild(serverid)
        channel = guild.text_channels[0]
        await channel.send(random.randint(1,1000))


@client.event
async def on_message(message: selfcord.Message):
    print(message.content,'on_message')
    global catchball


    if message.content == 'show comp':
        commands = [command async for command in message.channel.slash_commands()]
        for command in commands:
            if command.name == 'balls':
                for subcommand in command.children:
                    if subcommand.name == 'completion':
                        await subcommand.__call__(channel=message.channel, user=message.author)

    if 'give ball ' in message.content:
        hexid = message.content.split(' ',2)[2]
        if hexid[0] == '#':
            hexid = hexid[1:]
        commands = [command async for command in message.channel.slash_commands()]
        for command in commands:
            if command.name == 'balls':
                for subcommand in command.children:
                    if subcommand.name == 'give':
                        await subcommand.__call__(channel=message.channel, user=message.author, countryball=int(hexid, 16))

        # slashCmds = client2.getSlashCommands('999736048596816014').json()
        # s = SlashCommander(slashCmds)
        # data = s.get(['completion'])
        # client2.triggerSlashCommand('999736048596816014', str(message.channel.id), guildID=str(message.guild.id), data=data)

    if message.author.id == 999736048596816014: #ballsdex
        if message.content == 'A wild countryball appeared!':
            img_url = message.attachments[0].url
            ball = predict_category(img_url)
            catchball.append(ball)
            interaction = await message.components[0].children[0].click()
        

        elif f'<@{client.user.id}> You caught' in message.content:
            mention = '<@707866373602148363>'
            stats = message.content.split('`(',1)[1].split(')`',1)[0]
            ball = message.content.split('You caught **',1)[1].split('!',1)[0]
            special = ''
            if 'mythical aura' in message.content:
                special = f' (MYTHICAL!!!) {mention}'
            if 'shiny countryball' in message.content:
                special = f' (SHINY) {mention}'
            if 'new countryball' in message.content:
                special = ' (New)'
            
            catchmsg = f'Caught {ball} ({stats}){special} {message.jump_url}'
            print(catchmsg)
            webhook = DiscordWebhook(url=webhookurl, content=catchmsg)
            response = webhook.execute()

        elif message.content == f'<@{client.user.id}> Wrong name!':
            print(f'{ball} missed in {message.guild.name}')
        
    
    
    # if message.guild.id == 1254513690976325742: #chog server
    #     if message.author.id == 1268008744877424640: #testdex
    #         if message.content == 'A wild countryball appeared!':
    #             # img_url = message.attachments[0].url
    #             # ball = predict_category(img_url)
    #             catchball.append('test123')
    #             print('before interaction')
    #             await asyncio.sleep(1)
    #             interaction = await message.components[0].children[0].click()

@client.event
async def on_modal(modal: selfcord.Modal):
    global catchball
    modal.components[0].children[0].answer(catchball[-1])
    await modal.submit()

@client.event
async def on_message_edit(before: selfcord.Message, message: selfcord.Message):
    # print(message.content,'on_edit')
    # if message.guild.id == 1254513690976325742: 
    #     return
    if message.author.id == 999736048596816014: # ballsdex
        if f'<@{client.user.id}> You caught' in message.content:
            stats = message.content.split('`(',1)[1].split(')`',1)[0]
            ball = message.content.split('You caught **',1)[1].split('!',1)[0]
            special = ''
            if 'mythical aura' in message.content:
                special = ' (Mythical)'
            if 'shiny countryball' in message.content:
                special = ' (Shiny)'
            if 'new countryball' in message.content:
                special = ' (New)'
            
            catchmsg = f'Caught {ball} ({stats}) {special} {message.jump_url}'
            print(catchmsg)
            webhook = DiscordWebhook(url=webhookurl, content=catchmsg)
            response = webhook.execute()

        if message.content == f'<@{client.user.id}> Wrong name!':
            special = ''
            print(f'{ball} missed in {message.guild.name}{special}')

# loop = asyncio.get_event_loop()
# loop.create_task(client.start())
# loop.create_task(client2.start(config['bot']['token2']))
# loop.run_forever()

client.run(config['bot']['token'])