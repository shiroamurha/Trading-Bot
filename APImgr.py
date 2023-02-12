from binance.client import Client
import json
from datetime import datetime



class TradingBotAPI():

    def __init__(self):

        keys = json.load(open('keys.json', 'r'))
    
        self.client = Client(keys['API_KEY'], keys['API_SECRET'])
        self.exchange_info = self.client.get_exchange_info()['symbols']

    def get_pair_price(self, pair):       
        return float(self.client.get_ticker(symbol=pair)["lastPrice"])     

    def create_limit_order(self, type, pair, quantity, price):

        pair = self.split_pair(pair)

        match type:
            case 'buy': 
                quantity = self.handle_percentage(type, pair, quantity, price)
                self.client.order_limit_buy(symbol=pair[2], quantity=quantity, price=price)
                
            case 'sell': 
                quantity = self.handle_percentage(type, pair, quantity, price)
                self.client.order_limit_sell(symbol=pair[2], quantity=quantity, price=price)
    
    def create_market_order(self, type, pair, quantity):

        pair = self.split_pair(pair)

        match type:

            case 'buy': 

                quantity = self.handle_percentage(type, pair, quantity, self.get_pair_price(pair[2]))
                order = self.client.order_market_buy(symbol=pair[2], quantity=quantity)

            case 'sell': 

                quantity = self.handle_percentage(type, pair, quantity, self.get_pair_price(pair[2]))
                order = self.client.order_market_sell(symbol=pair[2], quantity=quantity)
                
        return order['status']

    def await_simultaneous_orders(self, type, order_1: dict(), order_2: dict()):

        # method call template: 
        #   await_simultaneous_orders(
        #       'buy', 
        #       {'pair':'BTC/BUSD', 'quantity':0.001, 'price':24000}, 
        #       {'pair':'MATIC/BUSD', 'quantity':15%, 'price':1.50}
        #   )

        # both orders should have one of the same currency on the pair ex: BTC/BUSD, MATIC/BUSD
        # both orders should have the same type of order: buy or sell 
        # loop will wait for the first price to be beaten and do a market order

        # method parameters treatment
        order_1['pair'] = self.split_pair(order_1['pair'])
        order_2['pair'] = self.split_pair(order_2['pair'])       
        
        order_1['quantity'] = self.handle_percentage(type, order_1['pair'], order_1['quantity'], order_1['price']) 
        order_2['quantity'] = self.handle_percentage(type, order_2['pair'], order_2['quantity'], order_2['price']) 

        price_1 = self.get_pair_price(order_1['pair'][2])
        price_2 = self.get_pair_price(order_2['pair'][2])

        # main worker loop checking the prices
        while True:
            
            if price_1 >= order_1['price']:

                order_status = self.create_market_order(type, order_1['pair'][2], order_1['quantity'])
                log = f'ORDER 1 DONE AT {str(datetime.now())[:19]}: \nSTATUS: {order_status}\n [{order_1["pair"][2], order_1["quantity"], price_1}]'
                old_logs = open('logs.txt', 'r').read()                
                with open('logs.txt', 'w') as write_logs:
                    write_logs.write(f'{old_logs}\n{log}')
                
                print(log)
                break

            elif price_2 >= order_2['price']:

                order_status = self.create_market_order(type, order_2['pair'][2], order_2['quantity'])
                
                log = f'ORDER 2 DONE AT {str(datetime.now())[:19]}: \nSTATUS: {order_status}\n [{order_2["pair"][2], order_2["quantity"], price_2}]'
                old_logs = open('logs.txt', 'r').read()                
                with open('logs.txt', 'w') as write_logs:
                    write_logs.write(f'{old_logs}\n{log}')
                
                print(log)
                break
            
            else:
                price_1 = self.get_pair_price(order_1['pair'][2])
                price_2 = self.get_pair_price(order_2['pair'][2])
                continue
    
    def handle_percentage(self, type, pair, quantity, price):

        match type:
            case 'buy': 

                if quantity.find('%') > 0: 
                    # i.e. if there is '%' in the quantity
                    quantity = float(quantity.replace('%', ''))
                    balance = self.client.get_asset_balance(pair[1])['free']
                    quantity = (float(balance) * quantity / 100)

                else: 
                    quantity = float(quantity)

            case 'sell': 

                if quantity.find('%') > 0: 
                    # i.e. if there is '%' in the quantity
                    quantity = float(quantity.replace('%', ''))
                    balance = float(self.client.get_asset_balance(pair[0])['free'])
                    quantity = (balance * quantity / 100)
                else: 
                    quantity = float(quantity)

        precision = self.get_currency_precision(pair[2])
        quantity = int(quantity * 10**precision) / 10**precision

        return quantity


    def split_pair(self, pair):

        pair = pair.split('/') # 'ABC/DEF' -> ['ABC','DEF'] 
        pair.append(str().join(pair)) # ['ABC','DEF', 'ABCDEF'] 

        return pair


    def get_currency_precision(self, pair):

        for symbol in self.exchange_info:

            if symbol['symbol'] == pair:

                precision = symbol['filters'][1]['stepSize']
                precision = str(precision).find('1') - 1 

                if precision == -1:
                    return 0
                else:
                    return precision
    # def fee(self):
    #     print(self.client.get_trade_fee(symbol='AXSBNB'))

if __name__ == "__main__":

    """

        da pra tirar tudo de comentario selecionando os bagulhos e apertando ctrl + ;

        isso aqui se chama docstring, é tipo um comentario pirocudo
        
    """  

    # examples:

    api = TradingBotAPI()
    print(api.handle_percentage('sell', ['BTC','BRL','BTCBRL'], '100%', 115800.1))
    #api.create_market_order('buy', 'AXS/BTC', '100%')
    # api.await_simultaneous_orders(
    #       'buy', 
    #       {'pair':'BTC/BUSD', 'quantity':0.001, 'price':24000}, 
    #       {'pair':'MATIC/BUSD', 'quantity': '15%', 'price':1.50}
    # )

    # api.create_limit_order('buy', 'NEAR/USDT', '100%', 2.150)
    
    # api.create_market_order('buy', 'BNB/USDT', '100%')