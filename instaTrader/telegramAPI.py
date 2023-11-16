import asyncio
from telethon.sync import TelegramClient
from telethon import events
import datetime
import kucoinAPI



amount = 13.0
channel_link = 't.me/TodayWePush' 
#   t.me/TodayWePush
#   t.me/+dfOF0OmHl6YwMjQ9 big pumps
trade_datetime = {
    "day": "05", 
    "hour": 14
}

trade_datetime['before'] = f'{trade_datetime.get("day")} {trade_datetime.get("hour") - 1}'
trade_datetime['exact'] = f'{trade_datetime.get("day")} {trade_datetime.get("hour")}'



def login_telegram():
    global client
    telethon_keys = [
        '', 
        '', 
        '6473434844:AAEjB63mfg7dqtlzAzkSNQZVLxOQMDWfMJ4'
    ]

    client = TelegramClient('shiro', telethon_keys[0], telethon_keys[1])
    client.start() # bot_token=telethon_keys[2]

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

async def wait_for_datetime():

    while str(datetime.datetime.now())[8:13] != trade_datetime.get('before'): #'day hour' -> '8 14'
        #print(str(datetime.datetime.now())[9:13])
        await asyncio.sleep(0.1)

    print('passed threshold time: 1 hour left')



async def check_message():
    global globalpair, channel_link

    while str(datetime.datetime.now())[8:13] != trade_datetime.get('exact'): #8 14h
        await asyncio.sleep(0.1)

    print('passed exact time: les go xd')
    channel_id = await client.get_entity(channel_link) 

    while True:
        await asyncio.sleep(0.8)

        async for message in client.iter_messages(channel_id, limit=1):
            globalpair = extract_coin_from(message.text)
            # print(globalpair, message.text)
            if globalpair is not None:
                client.disconnect()
                break



def main():
    
    global amount, globalpair

    asyncio.get_event_loop().run_until_complete(wait_for_datetime())
    kucoinAPI.login()
    
    try:
        login_telegram()
        client.loop.run_until_complete(check_message())

    except ConnectionError: # when it finds the coin it disconects from telethon
        kucoinAPI.insta_buySell(amount, globalpair)
        
    print(globalpair)      



if __name__ == '__main__':
    main()
