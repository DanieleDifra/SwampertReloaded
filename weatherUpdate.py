import paho.mqtt.publish as publish
import psutil
import string
import time
from logging import exception
import requests
import sys
import random
import telepot

## ThingSpeak Channel connection
channel_ID = "1806671"
mqtt_host = "mqtt3.thingspeak.com"
mqtt_client_ID = "ITgGHjUoFwwZEDIUPCgIJS8"
mqtt_username  = "ITgGHjUoFwwZEDIUPCgIJS8"
mqtt_password  = "51bdD9cJODXzePgbKtaNFKQk"
t_transport = "websockets"
t_port = 80
topic = "channels/" + channel_ID + "/publish"

def getWeather():
    weather_url = "http://dataservice.accuweather.com/currentconditions/v1/214046?apikey=GoxexX06khkOOTkiUFNfFB0Lh0tnAo1x"
    response = requests.get(weather_url)
    if response.status_code == 200:
       json_response = json.loads(response.text)
       return json_response
    else:
       return exception 

weather = getWeather()
temp = str(weather[0]['Temperature']['Metric']['Value'])
payload = "field4=" + temp

try:
    print ("Writing Payload = ", payload," to host: ", mqtt_host, " clientID= ", mqtt_client_ID, " User ", mqtt_username, " PWD ", mqtt_password)
    publish.single(topic, payload, hostname=mqtt_host, transport=t_transport, port=t_port, client_id=mqtt_client_ID, auth={'username':mqtt_username,'password':mqtt_password})
except Exception as e:
        print (e)

