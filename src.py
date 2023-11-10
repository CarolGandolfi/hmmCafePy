import telegram
import asyncio
import RPi.GPIO as gpio
import time
import aiohttp

PIN1=00   # Usando modo BCM
PIN2=07

async def sendToTelegram(message):
    bot = telegram.Bot(token='6484292851:AAG0odJEkLZ33PbZi7uxrFmkNuDEXuhHdmU')
    await bot.send_message(chat_id='-4067332732', text=message)

 
def gpioListener(pin1, pin2):
    while True:
        if gpio.input(pin1) == gpio.HIGH:
            asyncio.run(sendToTelegram('Nível do galão baixo... Convém reabastecer!'))
            asyncio.run(http_request_ifttt('galao_vazio'))

        else:
            asyncio.run(sendToTelegram('Galão reabastecido!!'))

        if gpio.input(pin2) == gpio.HIGH:
            asyncio.run(http_request_ifttt('reservatorio_cafeteira'))

        time.sleep(1)


def main():
    gpioListener(PIN1, PIN2)

async def http_request_ifttt(event_name):
    try:
        url = "https://maker.ifttt.com/trigger/cafeteira_event/with/key/fSRoSbSiX_JywuqSNYyDUBBDHXWq2Y02k1Yd4Tm1uzC"
        params = {'value1': event_name}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                response_text = await response.text()
                print("Resposta da solicitação GET:")
                print(response_text)

    except aiohttp.ClientError as e:
        print(f"Erro na solicitação GET: {e}")
 
 
#Configurando GPIO
# Configurando o modo dos pinos como BCM
gpio.setmode(gpio.BCM)
 
# Configurando PIN1 e PIN2 como INPUT
gpio.setup(PIN1, gpio.IN)
gpio.setup(PIN2, gpio.IN)

main()

gpio.cleanup()
exit()


