import os
from PIL import Image
from keras._tf_keras.keras.models import load_model
import numpy as np
from keras._tf_keras.keras.preprocessing.image import img_to_array
from io import BytesIO
import requests
os.chdir(os.path.dirname(os.path.abspath(__file__)))
path = os.path.abspath(os.path.join(os.pardir,'model.keras'))
if not os.path.isfile(path):
    print('downloading model file...')
    r = requests.get('https://files.catbox.moe/6y5m80.keras')
    with open(path,'x+') as file:
        file.write(r.content)
    print('downloaded model file!')

model = load_model(path)
image_size = (128, 128)

countryballs = ['British Empire', 'Reichtangle', 'Russian Empire', 'Mongol Empire', 'Kalmar Union', 'Roman Empire', 'Polish-Lithuanian Commonwealth', 'Qin Dynasty', 'German Empire', 'Holy Roman Empire', 'Austria-Hungary', 'Hunnic Empire', 'Japanese Empire', 'Republic of China', 'Soviet Union', 'United States', 'Vatican', 'Russia', 'China', 'Austrian Empire', 'India', 'Ancient Greece', 'Japan', 'Korea', 'Napoleonic France', 'Ottoman Empire', 'Republic of Venice', 'South Korea', 'France', 'Spanish Empire', 'Achaemenid Empire', 'Macedon', 'United Kingdom', 'Pakistan', 'Ancient Egypt', 'Brazil', 'Byzantium', 'Greenland', 'Portuguese Empire', 'Qing', 'British Raj', 'Carthage', 'Italy', 'Kingdom of Italy', 'Egypt', 'Russian Soviet Federative Socialist Republic', 'Turkey', 'French Empire', 'Iran', 'Kingdom of Greece', 'African Union', 'Arab League', 'Kingdom of Hungary', 'Confederate States', 'Gaul', 'Germania', 'Indonesia', 'Mayan Empire', 'Yugoslavia', 'Germany', 'Australia', 'Hong Kong', 'Israel', 'Xiongnu', 'Swedish Empire', 'Spain', 'Antarctica', 'Ming Dynasty', 'Saudi Arabia', 'Franks', 'League of Nations', 'Monaco', 'Union of South Africa', 'Ukraine', 'Canada', 'Poland', 'Kingdom of Brandenburg', 'Sweden', 'Macau', 'Scotland', 'South Africa', 'Greece', 'Vietnam', 'Safavid Empire', 'Thailand', 'Parthian Empire', 'North Korea', 'England', 'European Union', 'Francoist Spain', 'Manchukuo', 'NATO', 'Republican Spain', 'United Arab Republic', 'United Nations', 'Warsaw Pact', 'Weimar Republic', 'Zhou', 'Yuan Dynasty', 'Algeria', 'Argentina', 'Bangladesh', 'Colombia', 'Czechia', 'Iraq', 'Malaysia', 'Mexico', 'Myanmar', 'Netherlands', 'Nigeria', 'Norway', 'Peru', 'Philippines', 'Portugal', 'Prussia', 'Romania', 'Singapore', 'Switzerland', 'Syria', 'Tuvalu', 'UAE', 'Venezuela', 'Mali Empire', 'Ukrainian Soviet Socialist Republic', 'Ancient Athens', 'Ancient Sparta', 'Babylon', 'Czechoslovakia', 'Ethiopian Empire', 'French Indochina', 'Nauru', 'Numidia', 'Quebec', 'Siam', 'South Vietnam', 'Taiwan', 'Wales', 'West Germany', 'Cuba', 'Kingdom of Egypt', 'Mughal Empire', 'Angola', 'Austria', 'Azerbaijan', 'Bahamas', 'Belarus', 'Belgium', 'Bolivia', 'Bulgaria', 'Chile', 'Croatia', 'Cyprus', 'DR Congo', 'Denmark', 'Ecuador', 'Ethiopia', 'Finland', 'Hungary', 'Jordan', 'Kazakhstan', 'Kenya', 'Kuwait', 'Libya', 'Morocco', 'North Vietnam', 'Oman', 'Qatar', 'San Marino', 'Serbia', 'Slovakia', 'Sri Lanka', 'Sudan', 'Tunisia', 'Turkmenistan', 'Uzbekistan', 'Yemen', 'Iberian Union', 'Faroe Islands', 'Trinidad and Tobago', 'East Germany', 'Free France', 'Jamaica', 'Maldives', 'Northern Ireland', 'Tibet', 'Golden Horde', 'Vichy France', 'Andorra', 'Brunei', 'Byelorussian Soviet Socialist Republic', 'Micronesia', 'Tonga', 'Grand Duchy of Tuscany', 'Khedivate of Egypt', 'Khmer Empire', 'Barbados', 'Marshall Islands', 'Armenia', 'Bahrain', 'Cambodia', 'Chad', 'Equatorial Guinea', 'Congo Free State', 'Georgia', 'Ghana', 'Guatemala', 'Guyana', 'Ireland', 'Kyrgyzstan', 'Latvia', 'Lithuania', 'Mali', 'Malta', 'Fatimid Caliphate', 'Mongolia', 'New Zealand', 'Samoa', 'Slovenia', 'Togo', 'Uganda', 'Uruguay', 'Zambia', 'Zimbabwe', 'Malawi', 'Kingdom of Sardinia', 'Costa Rica', 'Dominica', 'Guinea-Bissau', 'Sao Tome and Principe', 'Tannu Tuva', 'Seychelles', 'Afghanistan', 'Albania', 'Belize', 'Bosnia and Herzegovina', 'Botswana', 'Cameroon', 'Ceylon', 'Congo', "Cote d'Ivoire", 'Dominican Republic', 'Eritrea', 'Estonia', 'Eswatini', 'Fiji', 'Free City of Danzig', 'Gambia', 'Haiti', 'Honduras', 'Khiva', 'Laos', 'Lebanon', 'Liechtenstein', 'Moldova', 'Mozambique', 'Nepal', 'Nicaragua', 'Niger', 'Palestine', 'Paraguay', 'Saint Kitts and Nevis', 'Saint Lucia', 'Somaliland', 'South Sudan', 'South Yemen', 'Tajikistan', 'Tanzania', 'Western Sahara', 'Cape Verde', 'Guinea', 'Grenada', 'Palau', 'St. Vincent and the Grenadines', 'Solomon Islands', 'Vanuatu', 'Principality of Moldavia', 'Qajar Dynasty', 'Antigua and Barbuda', 'Benin', 'Majapahit', 'Bhutan', 'Burkina Faso', 'Nanda Empire', 'Burundi', 'Central African Republic', 'Comoros', 'El Salvador', 'Gabon', 'Hejaz', 'Iceland', 'Kiribati', 'Kosovo', 'Lesotho', 'Liberia', 'Luxembourg', 'Madagascar', 'Mauritania', 'Mauritius', 'Montenegro', 'Namibia', 'North Macedonia', 'Panama', 'Papua New Guinea', 'Paris Commune', 'Rwanda', 'Senegal', 'Sierra Leone', 'Somalia', 'Suriname', 'Timor-Leste', 'Djibouti']
sorted = countryballs.copy()
sorted.sort()

def makePrediction(img_url):
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content)).convert('RGB')

    img = img.resize(image_size)
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions, axis=1)
    return sorted[list(predicted_class)[0]]