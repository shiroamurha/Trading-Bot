import kucoin.client as kc
import json
from telethon.sync import TelegramClient
from telethon import events
from datetime import datetime
import asyncio

# Set your API Key and API Secret here
API_KEY = ''
API_SECRET = ''

# Initialize the KuCoin client outside of the function
kucoin_client = kc.Client(API_KEY, API_SECRET, 'passphrase')

# Initialize the Telegram client
api_id = ''  # Replace with your Telegram API ID
api_hash = ''  # Replace with your Telegram API hash
telegram_client = TelegramClient('anon', api_id, api_hash)

# Dictionary that maps channel usernames to message templates and trade percentages
channel_message_templates = {
    'kopkplxcvb': {'template': 'the coin is :', 'percentage': 1.4},
    'asdf12esds': {'template': 'COIN:', 'percentage': 1.2},
    # Add more channels, templates, and percentages as needed
}

# Counter to keep track of successful trades
trade_counter = 0

# Default trade percentage
default_trade_percentage = 1.5  # You can change this to your desired default percentage

def trade_on_kucoin(pair, buy_quantity, trade_percentage):
    global trade_counter  # Use global variable to update the counter
    price = float(kucoin_client.get_ticker(f'{pair}-USDT').get('price'))
    # Calculate the percentage based on the trade_percentage parameter
    after_price = int(price * trade_percentage * 100000000) / 100000000
    buy_order = kucoin_client.create_market_order(f'{pair}-USDT', 'buy', funds=buy_quantity)
    accounts = kucoin_client.get_accounts()

    for item in accounts:
        if item.get('currency') == pair and item.get('type') == 'trade':
            sell_quantity = int(float(item.get('available')) * 100000000) / 100000000

    sell_order = kucoin_client.create_limit_order(f'{pair}-USDT', 'sell', after_price, sell_quantity)

    json.dump(kucoin_client.get_accounts(), open('account.json', 'w'), indent=4)
    
    trade_counter += 1  # Increment the successful trade counter
    print(f'Trade percentage used: {trade_percentage}')

async def extract_currency_name(text, channel_username):
    if channel_username in channel_message_templates:
        template_info = channel_message_templates[channel_username]
        template = template_info['template']
        trade_percentage = template_info.get('percentage', default_trade_percentage)
        if template in text:
            parts = text.split(":")
            if len(parts) > 1:
                currency_name = parts[1].strip()
                return currency_name, trade_percentage
    return None, default_trade_percentage

async def send_periodic_message(client, channel_username, message):
    await client.start()
    channel = await client.get_entity(channel_username)

    while True:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message_with_time = f'[{current_time}] {message}'

        await client.send_message(channel, message_with_time)
        await asyncio.sleep(30)  # Wait for 30 seconds before sending the next message

async def send_successful_trade_message(client, channel_username, currency_name, trade_counter):
    await client.start()
    channel = await client.get_entity(channel_username)

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message = f'[{current_time}] Successfully. || Trade counter: [{trade_counter}] || Coin: [{currency_name}].'

    await client.send_message(channel, message)

# List of channel usernames to listen to
channels_to_listen = ['kopkplxcvb', 'asdf12esds']   # Add more channels as needed

# Function to listen to a specific channel
async def listen_to_channel(channel_username):
    await telegram_client.start()
    channel = await telegram_client.get_entity(channel_username)

    @telegram_client.on(events.NewMessage(chats=channel))
    async def new_message(event):
        current_time = datetime.fromtimestamp(event.date.timestamp()).strftime('%Y-%m-%d %H:%M:%S')
        text = event.message.text

        print(f'[{current_time}] New message in {channel_username}: {text}')

        currency_name, trade_percentage = await extract_currency_name(text, channel_username)

        if currency_name:
            print(f'Extracted currency name: {currency_name}')
            print(f'Using trade percentage: {trade_percentage}')

            trade_on_kucoin(currency_name, buy_quantity=3, trade_percentage=trade_percentage)

            print('Trade executed. Output message sent to telegram.')

            # Send a message when a trade is successful            # change this channel
            await send_successful_trade_message(telegram_client, 'money_stats', currency_name, trade_counter)

# Function to send messages periodically before listening to channels
async def send_periodic_messages():
    while True:                                        # change this channel
        await send_periodic_message(telegram_client, 'money_stats', "I am running.")

# Start the event loop to send messages periodically
async def main():
    await asyncio.gather(send_periodic_messages(), *(listen_to_channel(channel) for channel in channels_to_listen))

# Start the program
if __name__ == '__main__':
    asyncio.run(main())
