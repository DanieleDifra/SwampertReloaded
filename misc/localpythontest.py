from logging import exception
import requests
import json

def getWeather():
    weather_url = "http://dataservice.accuweather.com/currentconditions/v1/214046?apikey=GoxexX06khkOOTkiUFNfFB0Lh0tnAo1x"
    response = requests.get(weather_url)
    if response.status_code == 200:
       json_response = json.loads(response.text)
       return json_response
    else:
       return exception       

weather = getWeather()
temp = weather[0]['Temperature']['Metric']['Value']
print(temp)