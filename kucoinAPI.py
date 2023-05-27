import kucoin.client as kc
import json


def login():

    global client
    API_KEY = 'public key'                      #        test'64710815ba02b40001f9cc3d'
    API_SECRET = 'secret key'       #        test 'b03e7827-4c1f-4064-84d7-c8c6758c38ad'

    client = kc.Client(API_KEY, API_SECRET, 'passphrase')


def main():

    login()

    buy_quantity = 9.61 ## value in USDT to use

    pair = input('currency: ') # any
    price = float(client.get_ticker(f'{pair}-USDT').get('price'))

    buy_order = client.create_market_order(f'{pair}-USDT', 'buy', funds=buy_quantity)
    accounts = client.get_accounts()

    for item in accounts:
        if item.get('currency') == pair and item.get('type') == 'trade':
            sell_quantity = int(float(item.get('available')) * 100000000)/100000000
   
    after_price = int(price * 1.5 * 100000000)/100000000   #truncating long float numbers to only 10^-8 precision
                            # 1.5 is the price ratio to sell (+50%) 
    sell_order = client.create_limit_order(f'{pair}-USDT', 'sell', after_price, sell_quantity)

    json.dump(client.get_accounts(), open('account.json', 'w'), indent=4)

if __name__ == '__main__':
    main()
    

#client.get_ticker('BTC-USDT').get('price')