#!/usr/bin/env python3
from influxdb import InfluxDBClient
import requests
import json

# This app connects to an influxdatabase and puts in information from openweatherapp in there
# for further processes

influxdb_host = "<hostdbip>"
influxdb_port = '8086'
influxdb_database = 'weather'

dbusername = 'admin'
dbpassword = 'adminpw'


client = InfluxDBClient(host=influxdb_host, port=influxdb_port,
                        username=dbusername, password=dbpassword)
databases = client.get_list_database()
databaseAlreadyThere = False


for item in databases:
    if item['name'] == influxdb_database:
        databaseAlreadyThere = True

if databaseAlreadyThere == False:
    client.create_database(influxdb_database)

client.switch_database(influxdb_database)


#insert your openweather api url here
response = requests.get(
    'http://api.openweathermap.org/data/2.5/weather?q=berlin&appid=5db43f9f95059343c1d07d3084641680')
data = json.loads(response.content.decode('utf-8'))


json_bodies = []
json_body = []
jb = {}
tags = {}
fields = {}

# weather description
weather = data['weather'][0]
fields['weatherdata'] = weather

tags['mainweather'] = str(weather['main'])
tags['description'] = str(weather['description'])

# weatherapp default in celvin instead celcius
tags['temp'] = round(float(data['main']['temp']-273.15), 2)
tags['feels_like'] = round(float(data['main']['temp']-273.15), 2)
tags['temp_min'] = round(float(data['main']['temp_min']-273.15), 2)
tags['temp_max'] = round(float(data['main']['temp_max']-273.15), 2)
tags['pressure'] = float(data['main']['pressure'])
tags['humidity'] = float(data['main']['humidity'])

# wind
tags['speed'] = float(data['wind']['speed'])
tags['deg'] = float(data['wind']['deg'])
tags['gust'] = float(data['wind']['gust'])

tags['clouds'] = float(data['clouds']['all'])
tags['city'] = data['name']

lon = float(data['coord']['lon'])
lat = float(data['coord']['lat'])

jb['tags'] = tags
jb["measurement"] = "WeatherForecast"
jb['fields'] = tags

json_body.append(jb)
client.write_points(json_body, protocol=u'json', consistency='all')

