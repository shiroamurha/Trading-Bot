import kucoin.client as kc
import kucoin.exceptions as kc_ex



def login(key, secret, passphrase):

    global client

    API_KEY = key 
    API_SECRET = secret 
    PASSPHRASE = passphrase
    
    client = kc.Client(API_KEY, API_SECRET, passphrase = PASSPHRASE)


def insta_buySell(buy_quantity, pair, percentage):


    # gets the price of th pais
    price = float(client.get_ticker(f'{pair}-USDT').get('price'))

    # place market order
    buy_order = client.create_market_order(f'{pair}-USDT', 'buy', funds=buy_quantity)

    # gets coin info and account currencies info
    accounts = client.get_accounts()
    all_symbols = client.get_symbols()

    # searches the precision 
    for symbol in all_symbols:
        if symbol.get('symbol') == f'{pair}-USDT':
            precision = symbol.get('priceIncrement').count('0')
            break
    precision = 10**precision

    # searches the amount that was buyed in the market order
    for item in accounts:
        if item.get('currency') == pair and item.get('type') == 'trade':
            sell_quantity = float(item.get('available'))

    after_price = int(price * percentage * precision)/precision  # truncating long float numbers to the supported precision

    # places the limit order with the gotten info
    sell_order = client.create_limit_order(f'{pair}-USDT', 'sell', after_price, sell_quantity)
    print(f'  < orders placed >')
