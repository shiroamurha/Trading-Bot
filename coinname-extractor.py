import kucoin.client as kc
import json
from telethon.sync import TelegramClient
from telethon import events
from datetime import datetime

# Defina sua API Key e API Secret aqui
global client
API_KEY = ''                     
API_SECRET = '' 

# Inicialize o cliente da KuCoin fora da função
client_kucoin = kc.Client(API_KEY, API_SECRET, 'Shell.hydr4')

# Inicialize o cliente do Telegram

api_id = ''  # Substitua com seu API ID do Telegram
api_hash = ''  # Substitua com seu API hash do Telegram

client_telegram = TelegramClient('anon', api_id, api_hash)

def trade_on_kucoin(pair, buy_quantity):
    price = float(client_kucoin.get_ticker(f'{pair}-USDT').get('price'))
    buy_order = client_kucoin.create_market_order(f'{pair}-USDT', 'buy', funds=buy_quantity)
    accounts = client_kucoin.get_accounts()

    for item in accounts:
        if item.get('currency') == pair and item.get('type') == 'trade':
            sell_quantity = int(float(item.get('available')) * 100000000) / 100000000

    after_price = int(price * 1.5 * 100000000) / 100000000  # Truncar números longos para precisão de 10^-8
    sell_order = client_kucoin.create_limit_order(f'{pair}-USDT', 'sell', after_price, sell_quantity)

    json.dump(client_kucoin.get_accounts(), open('account.json', 'w'), indent=4)

def extrair_nome_da_moeda(texto):
    if "the coin is :" in texto:
        partes = texto.split(":")
        if len(partes) > 1:
            nome_da_moeda = partes[1].strip()
            return nome_da_moeda
    return None

if __name__ == '__main__':
    import asyncio

    async def ouvir_novas_mensagens(channel_username):
        await client_telegram.start()

        # Obtenha o canal pelo nome de usuário
        channel = await client_telegram.get_entity(channel_username)

        @client_telegram.on(events.NewMessage(chats=channel))
        async def novo_mensagem(event):
            data_hora = datetime.fromtimestamp(event.date.timestamp()).strftime('%Y-%m-%d %H:%M:%S')
            texto = event.message.text

            print(f'[{data_hora}] Nova mensagem em {channel_username}: {texto}')

            # Extrair o nome da moeda da mensagem
            nome_da_moeda = extrair_nome_da_moeda(texto)

            if nome_da_moeda:
                print(f'Nome da moeda extraído: {nome_da_moeda}')

                # Realizar trade na KuCoin com base no nome da moeda
                trade_on_kucoin(nome_da_moeda, buy_quantity=3)

                print('Trade realizado com sucesso.')

        await client_telegram.run_until_disconnected()

    channel_username = ''
    asyncio.run(ouvir_novas_mensagens(channel_username))
