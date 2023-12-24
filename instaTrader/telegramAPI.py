import asyncio
from telethon.sync import TelegramClient
from telethon import events
import datetime



def login(id, hash):
    
    global client
    telethon_keys = [ id, hash ]

    client = TelegramClient('shiro', telethon_keys[0], telethon_keys[1])
    client.start() 

def extract_coin_from(message):
    
    message = message[::-1]
    coin = message[message.find('-')+1 : message.find('/')] 
    coin = coin[::-1]
    for char in coin:
        if char not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            return None
            
    return coin if coin != '' else None

    # reverse the message then get the part between a - and a / 
    # recieves 'pipipo https://www.kucoin.com/trade/SYNR-USDT'
    # then 'TDSU-RNYS/edart/moc.niocuk.www//:sptth opipip'
    # finds the indexes between - and /,  that corresponds to RNYS then reverts it again: SYNR
    # returns None if no coin is properly recieved, else returns the coin

async def wait_for_datetime(trade_datetime):

    while str(datetime.datetime.now())[8:13] != trade_datetime.get('before'): #'day hour' -> '8 14'
        #  ^  ^  ^  ^  ^  ^ returns 'DD HH' 
        await asyncio.sleep(1)

    print('passed threshold time: 1 hour left')



async def check_message(channel_link, trade_datetime):

    global globalpair 

    # waits for exact time, 5 seconds before the schedule hour
    while str(datetime.datetime.now())[8:19] != trade_datetime.get('exact'): #8 14h
        await asyncio.sleep(0.2)

    print('passed exact time: les go xd')
    channel_id = await client.get_entity(channel_link)  

    while True:
        await asyncio.sleep(0.6)

        # every half a second checks the last message in the channel
        async for message in client.iter_messages(channel_id, limit=1):

            globalpair = extract_coin_from(message.text)
            # print(globalpair, message.text) testing shit

            # if the function returned a coin then disconect from telethon
            if globalpair is not None:
                client.disconnect()
                break
