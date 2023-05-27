import kucoin.client as kc
import json



API_KEY = '64710815ba02b40001f9cc3d'
API_SECRET = 'b03e7827-4c1f-4064-84d7-c8c6758c38ad'

client = kc.Client(API_KEY, API_SECRET, 'shiro123', sandbox=True)



buy_quantity = 100.0
pair = input('par: ') #'BTC'
price = float(client.get_ticker(f'{pair}-USDT').get('price'))

buy_order = client.create_market_order(f'{pair}-USDT', 'buy', funds=buy_quantity)

accounts = client.get_accounts()

for item in accounts:
    if item.get('currency') == pair and item.get('type') == 'trade':
        sell_quantity = item.get('available')
    
after_price = price * 1.5
sell_order = client.create_limit_order(f'{pair}-USDT', 'sell', after_price, sell_quantity)

json.dump(client.get_accounts(), open('account.json', 'w'), indent=4)
#client.get_ticker('BTC-USDT').get('price')