import kucoinAPI as kc
import telegramAPI as tg
import asyncio
from json import load, loads



def get_assets(_ = "imports all configs from the json file"):

    global assets
    global trade_datetime

    assets = load(open('settings.json', 'r'))

    # transforming raw percentage into a multiplier, e.g. 35% -> 1.35
    percentage = assets.get('TRADE-ASSETS').get('percentage')
    percentage = percentage * 0.01 + 1
    assets['TRADE-ASSETS'].update({'percentage': percentage})

    trade_datetime = {
        "day":  assets['TRADE-ASSETS'].get('trade_datetime')[0], # corresponding to the day
        "hour": assets['TRADE-ASSETS'].get('trade_datetime')[1]  #                      hour
    }

    # fixing day str if its only 1 digit wide
    if len(str(trade_datetime['day'])) == 1:
        trade_datetime['day'] =  f'0{trade_datetime["day"]}'
    
    # translating into readable datetimes
    trade_datetime['before'] = f'{trade_datetime.get("day")} {trade_datetime.get("hour")-1}'
    trade_datetime['exact'] = f'{trade_datetime.get("day")} {trade_datetime.get("hour")-1}:59:55'

   
####### 
   

def main():

    get_assets()

    # waits to the before time, 1h before the schedule
    asyncio.get_event_loop().run_until_complete(tg.wait_for_datetime(trade_datetime))

    kc.login(
        assets['KEYS'].get('KC-KEY'), 
        assets['KEYS'].get('KC-SECRET'), 
        assets['KEYS'].get('KC-PASSPHRASE')
    )
    
    try:
        tg.login(
            assets['KEYS'].get('TG-ID'),
            assets['KEYS'].get('TG-HASH')
        )

        # waits to the time and sends periodic requests checking the messages in the channel
        tg.client.loop.run_until_complete(
            tg.check_message(
                assets['TRADE-ASSETS'].get('channel_link'), 
                trade_datetime
            )
        )

    except ConnectionError: # when it finds the coin it disconects from telethon

        print(tg.globalpair)

        # function call to place the orders
        kc.insta_buySell(
            assets['TRADE-ASSETS'].get('amount'), 
            tg.globalpair, 
            assets['TRADE-ASSETS'].get('percentage')
        )
  
         

if __name__ == '__main__':
    main()