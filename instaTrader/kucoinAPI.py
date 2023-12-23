import kucoin.client as kc



def login():

    global client
    API_KEY = ''                      #        test'64710815ba02b40001f9cc3d'
    API_SECRET = ''       #        test 'b03e7827-4c1f-4064-84d7-c8c6758c38ad'

    client = kc.Client(API_KEY, API_SECRET, passphrase = 'shiro123')


def insta_buySell(buy_quantity, pair, percentage):

    # buy_quantity = 5.70 ## value in USDT to use

    # pair = input('currency: ') # any
    price = float(client.get_ticker(f'{pair}-USDT').get('price'))

    buy_order = client.create_market_order(f'{pair}-USDT', 'buy', funds=buy_quantity)
    accounts = client.get_accounts()
    all_symbols = client.get_symbols()

    for symbol in all_symbols:
        if symbol.get('symbol') == f'{pair}-USDT':
            precision = symbol.get('priceIncrement').count('0')
            break
    precision = 10**precision

    for item in accounts:
        if item.get('currency') == pair and item.get('type') == 'trade':
            sell_quantity = float(item.get('available'))

    after_price = int(price * percentage * precision)/precision  #truncating long float numbers to the supported precision
                            # 1.35 is the price ratio to sell (+35%) 
    print(f'{price} - {after_price} - {sell_quantity}')
    sell_order = client.create_limit_order(f'{pair}-USDT', 'sell', after_price, sell_quantity)
