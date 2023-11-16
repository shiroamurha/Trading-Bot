import kucoinAPI as kc
import telegramAPI as tg
import asyncio



amount = 1.0 #USDT
trade_datetime = {
    "day": 19, 
    "hour": 14
}
channel_link = 't.me/TodayWePush' 
#   t.me/+tiRgWqoxKK01ZTAx test
#   t.me/TodayWePush
#   t.me/+dfOF0OmHl6YwMjQ9 big pumps

if len(str(trade_datetime['day'])) == 1:
    trade_datetime['day'] =  f'0{trade_datetime["day"]}'
    
trade_datetime['before'] = f'{trade_datetime.get("day")} {trade_datetime.get("hour") - 1}'
trade_datetime['exact'] = f'{trade_datetime.get("day")} {trade_datetime.get("hour")}'

   
####### 
   

def main():

    asyncio.get_event_loop().run_until_complete(tg.wait_for_datetime(trade_datetime))
    kc.login()
    
    try:
        tg.login()
        tg.client.loop.run_until_complete(tg.check_message(channel_link, trade_datetime))

    except ConnectionError: # when it finds the coin it disconects from telethon
        print(tg.globalpair)
        kc.insta_buySell(amount, tg.globalpair)
  
         

if __name__ == '__main__':
    main()         