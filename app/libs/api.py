import requests
from discord_webhook import DiscordWebhook # Wrapper para mandar mensaje al webhook de Discord
import logging

#? Weather API
def getForecast(api_key, location):
    url = "https://api.weatherapi.com/v1/forecast.json?key={}&q={}&aqi=yes".format(api_key, location)

    response = requests.get(url, headers={'Connection':'close'})

    return response.json() # Return dictionary from json returned by server

def willRain(forecast):
    
    time_rain = [] 
    # List of hour that will rain on a day
    for hour in forecast['forecast']['forecastday'][0]['hour']:
        if hour['will_it_rain'] == 1:
            time_rain.append(hour['time'])

    return time_rain

#? Discord
def sendMessage(webhook, message):
    try:
        webhook = DiscordWebhook(url=webhook, content=message)
        response = webhook.execute()
        logging.info("Message sent to Discord")
    except: 
        logging.error("Sending message to Discord was not possible")