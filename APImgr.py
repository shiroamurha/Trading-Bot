from binance.client import Client
import json
from datetime import datetime



class TradingBotAPI():

    def __init__(self):

        keys = json.load(open('keys.json', 'r'))

        self.client = Client(keys['API_KEY'], keys['API_SECRET'])

    def get_pair_price(self, pair):       
        return self.client.get_ticker(symbol=pair)["lastPrice"]     

    def create_limit_order(self, type, pair, quantity, price):

        pair = self.split_pair(pair)

        match type:
            case 'buy': 

                if quantity.find('%') > 0: 
                    # i.e. if there is '%' in the quantity
                    quantity = float(quantity.replace('%', ''))
                    balance = self.client.get_asset_balance(pair[1])['free']
                    quantity = float(balance) * quantity / 100
                    
                else:
                    quantity = float(quantity)

                self.order = self.client.order_limit_buy(symbol=pair[2], quantity=quantity, price=price)
                

            case 'sell': 

                if quantity.find('%') > 0: 
                    # i.e. if there is '%' in the quantity
                    quantity = float(quantity.replace('%', ''))
                    balance = self.client.get_asset_balance(pair[0])['free']
                    quantity = float(balance) * quantity / 100
                else:
                    quantity = float(quantity)

                order = self.client.order_limit_sell(symbol=pair[2], quantity=quantity, price=price)
                
        return order # dict with orderId, symbol, origQty, price, side and status    keys
    
    def create_market_order(self, type, pair, quantity):

        pair = self.split_pair(pair)

        match type:
            case 'buy': 

                if quantity.find('%') > 0: 
                    # i.e. if there is '%' in the quantity
                    quantity = float(quantity.replace('%', ''))
                    balance = self.client.get_asset_balance(pair[1])['free']
                    quantity = float(balance) * quantity / 100
                else:
                    quantity = float(quantity)             

                order = self.client.order_limit_buy(symbol=pair, quantity=quantity)

            case 'sell': 

                if quantity.find('%') > 0: 
                    # i.e. if there is '%' in the quantity
                    quantity = float(quantity.replace('%', ''))
                    balance = self.client.get_asset_balance(pair[0])['free']
                    quantity = float(balance) * quantity / 100
                else:
                    quantity = float(quantity)

                order = self.client.order_limit_sell(symbol=pair, quantity=quantity)
                
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

        order_1['pair'] = self.split_pair(order_1['pair'])
        order_2['pair'] = self.split_pair(order_2['pair'])
        # -> 'pair': ['ABC', 'DEF','ABCDEF']

        if order_1['quantity'].find('%') > 0: 
            # i.e. if there is '%' in the quantity
            order_1['quantity'] = float(order_1['quantity'].replace('%', ''))

            match type:

                case 'buy':
                    balance = self.client.get_asset_balance(order_1['pair'][1])['free']
                    order_1['quantity'] = float(balance) * order_1['quantity'] / 100

                case 'sell':
                    balance = self.client.get_asset_balance(order_1['pair'][0])['free']
                    order_1['quantity'] = float(balance) * order_1['quantity'] / 100

        else:
            order_1['quantity'] = float(order_1['quantity'])

        if order_2['quantity'].find('%') > 0: 
            # i.e. if there is '%' in the quantity
            order_2['quantity'] = float(order_2['quantity'].replace('%', ''))

            match type:

                case 'buy':
                    balance = self.client.get_asset_balance(order_2['pair'][1])['free']
                    order_2['quantity'] = float(balance) * order_2['quantity'] / 100


                case 'sell':
                    balance = self.client.get_asset_balance(order_2['pair'][0])['free']
                    order_2['quantity'] = float(balance) * order_2['quantity'] / 100
        else:
            order_2['quantity'] = float(order_2['quantity'])
        

        price_1 = self.get_pair_price(order_1['pair'][2])
        price_2 = self.get_pair_price(order_2['pair'][2])

        while True:
            
            if price_1 >= order_1['price']:

                order_status = self.create_market_order(type, order_1['pair'][2], order_1['quantity'])
                print(f'ORDER 1 DONE AT {str(datetime.now())[:19]}: \nSTATUS: {order_status}\n [{order_1["pair"][2], order_1["quantity"], price_1}]')
                break

            elif price_2 >= order_2['price']:

                order_status = self.create_market_order(type, order_2['pair'][2], order_2['quantity'])
                print(f'ORDER 2 DONE AT {str(datetime.now())[:19]}: \nSTATUS: {order_status}\n [{order_2["pair"][2], order_2["quantity"], price_2}]')
                break
            
            else:
                price_1 = self.get_pair_price(order_1['pair'][2])
                price_2 = self.get_pair_price(order_2['pair'][2])
                continue
    
    def split_pair(self, pair):

        pair = pair.split('/') # 'ABC/DEF' -> ['ABC','DEF'] 
        pair.append(str().join(pair)) # ['ABC','DEF', 'ABCDEF'] 

        return pair



if __name__ == "__main__":

    """
        da pra tirar tudo de comentario selecionando os bagulhos e apertando ctrl + ;

        isso aqui se chama docstring, é tipo um comentario pirocudo
        
    """  

    # examples:

    api = TradingBotAPI()
    api.create_limit_order('buy', 'MATIC/BRL', '100%', 5.615)
    # print(api.get_pair_price('MATICBRL'))

    # api.await_simultaneous_orders(
    #       'buy', 
    #       {'pair':'BTC/BUSD', 'quantity':0.001, 'price':24000}, 
    #       {'pair':'MATIC/BUSD', 'quantity': '15%', 'price':1.50}
    # )

    # api.create_limit_order('buy', 'NEAR/USDT', '100%', 2.150)
    # api.create_market_order('buy', 'BNB/USDT', '100%')