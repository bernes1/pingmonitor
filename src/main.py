import os
import time
from loguru import logger
from twilio.rest import Client
from dotenv import load_dotenv, find_dotenv

# laster in env vaiablene med hemligheter
load_dotenv(find_dotenv())

# henter alle env variabler 
auth_token = os.getenv('Auth_Token')
account_sid = os.getenv('Account_sid')
smsnumber = os.getenv('smsnumber')j
brukertlf = os.getenv('Phone_Number')
msgaccount = os.getenv('messaging_service_sid')

# logging configutasjon 
logger.add(
    "file.log", format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")


# funksjon som komuniserer med Twilio sitt api og sender SMS
def varsle(service):
    #variabel som har authenifiserings info til twilio og initaliserer twiilio clienten 

    client = Client(account_sid, auth_token)
    #her sendes meldigen
    message = client.messages.create(
        from_= smsnumber,
        messaging_service_sid=msgaccount,
        body=f'!!!!ALERT!!!!\n server med ip:{service} er nede venligst sjekk serveren nå',
        to=brukertlf
    )


# funksjon som sjekker om host er oppe
def sjekker(hostname):
    response = os.system(f"ping -c 1 {hostname}")  # 
    # sjekker om respons er 0
    if response == 0:
        #når respons er 0 så er host oppe og skriver i loggen at host er oppe når 
        logger.debug(f"{hostname} is up")
    else:
        #sjekker om servern er faktisk nede og vennter 30 sec før den pinger serveren. hvis serveren er oppe så avslutter den if setiigen hvis ikke forsetter den vidre med og kjøre funksjoenen varsle 
        response = os.system(f"ping -c 1 {hostname}")
        logger.critical(f"{hostname} er urespnsive sjekker igjen om 30 sec")
        time.sleep(30)
        if response == 0:
            logger.critical(f"falsk alarm {hostname} er oppe!")
            return
        else:
            varsle(service=hostname)
            logger.critical(f"Varslet Bruker! host nede: {hostname}")


# while løkke som kjører under hele programmet og kaller på funksjoenen sjekker 
while True:
    ipaddresser = ["192.168.3.30", "68.183.65.22"]
    for ip in ipaddresser:
        sjekker(ip)
    time.sleep(300)
