from config import *
from service import APISource
from multiprocessing import Process


# Business logic For Sending Out Blasts Here

def run():
    "Start Everything"

    file = open(f"{cwd}/sources.json")
    data = json.load(file)

    # pull token in models
    tokens = data['tokens']

    for token in tokens:
        print(token["symbol"])
        print(token["address"])
        
        p = Process(target=start_streaming, name=token['symbol'], args=(token['symbol'], token['address']))
        p.start()



def start_streaming(symbol, address):
    "Start Streaming A Certain Token Address"
    token_data = {}
    logging.info(f"Provision {symbol} - {address}")

    client = APISource(address=address, symbol=symbol)
    contract = client.get_contract()
    if contract is not None:
        filters = client.get_buy_events()
    else:
        bot.send_message(
            TARGET_GROUP,
            f"🔔 Invalid Contract Address For {symbol} \n\n <b>Action Required 🔔🔔</b>"
        )
        logging.error(f"END STREAM (Invalid Contract Address)- {address}!!!")
        return

    while True:
        events = filters.get_new_entries()
        if events:

            try:
                res_data = client.get_buy_event_infura(Web3.toHex(events[0]['transactionHash']))
                tx_hash = res_data['result']['hash']

                data = client.get_tx_details(tx_hash, token_symbol=symbol)

                if data['buy_or_sell'] == 'buy':
                    logging.info(f"New Event!!! - {data}")
                    start_event(symbol, data)
                else:
                    logging.info("Not a valid Buy action")


            except Exception as e:
                    logging.error(f"Please check & fix bug - {e}")



def start_event(symbol, event):
    "Send Buy Event To Group"

    bot.send_message(
        TARGET_GROUP,
        f"<b>{event['name']} ({symbol})</b> Buy! \n🟢🟢🟢🟢🟢🟢 \
            \n\n 💵 {event['price']} ETH (${event['usd_value']}) \
            \n 🪪 <a href='https://etherscan.io/address/{event['address']}'>{event['address'][:5]}...{event['address'][-4:]}</a> | <a href='https://etherscan.io/tx/{event['tx_hash']}'>Txn</a>| Track \
            \n 🔘 Market Cap <b> ${event['market_cap']}</b> \
            \n\n <a href='https://dexscreener.com/ethereum/{event['contractAddress']}'>📊 Chart</a>",
        parse_mode="html",
        disable_web_page_preview=True
    )




if __name__ == "__main__":
    run()