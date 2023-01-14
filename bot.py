from config import *
from service import APISource


# Business logic For Sending Out Blasts Here

def run():
    "Start Everything"

    file = open(f"{cwd}/sources.json")
    data = json.load(file)

    # pull channels
    channels = data['channels']

    # pull token in models
    tokens = data['tokens']

    filters = {}
    token_data = {}

    for token in tokens:
        print(token["symbol"])
        print(token["address"])
        logging.info(f"Provision {token['symbol']} - {token['address']}")

        token_data[token['symbol']] = token['address']

        client = APISource(address=token["address"], symbol=token["symbol"])
        contract = client.get_contract()
        
        if contract is not None:
            filters[token["symbol"]] = client.get_buy_events()

        else:
            print("Invalid Contract Address!!!")

    while True:
        for symbol, event_filter in filters.items():
            events = event_filter.get_new_entries()
            if events:

                # Update preset contract addresses
                client.symbol = symbol
                client.address = token_data[symbol]
                print(events[0])

                res_data = client.get_buy_event_infura(Web3.toHex(events[0]['transactionHash']))
                tx_hash = res_data['result']['hash']

                data = client.get_tx_details(tx_hash, token_symbol=symbol)

                if data['buy_or_sell'] == 'buy':
                    logging.info(f"New Event!!! - {data}")
                    start_event(symbol, data)
                else:
                    print("Not a valid Buy action")



def start_event(symbol, event):
    "Send Buy Event To Group"
    print(event)
    bot.send_message(
        577180091,
        f"New {symbol} Buy Event - {event}"
    )


    bot.send_message(
        TARGET_GROUP,
        f"<a href='https://google.com'>{event['token_symbol']}</a> Buy! \n🟢🟢🟢🟢🟢🟢🟢🟢 \
            \n\n 💵 {event['price']} ETH (${event['usd_value']}) \
            \n 🪪 <a href='https://etherscan.io/address/{event['address']}'>{event['address'][:5]}...{event['address'][-4:]}</a> | <a href='https://etherscan.io/tx/{event['tx_hash']}'>Txn</a>| Track \
            \n 🔘 Market Cap <b> ${event['market_cap']}</b> \
            \n\n <a href='https://dexscreener.com/ethereum/{event['contractAddress']}'>📊 Chart</a>",
        parse_mode="html"
    )




if __name__ == "__main__":
    run()