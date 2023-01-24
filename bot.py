from config import *
from service import APISource
# from multiprocessing import Process


# Business logic For Sending Out Blasts Here


def start_streaming(symbol, address, tg_link='', icon='🟢'):
    "Start Streaming A Certain Token Address"
    token_data = {}
    logging.info(f"Provision {symbol} - {address}")

    client = APISource(address=address, symbol=symbol)
    contract = client.get_contract()
    if contract is not None:
        filters = client.get_buy_events()
    else:
        bot.send_message(
            -1001553783220,
            f"🔔 Invalid Contract Address For {symbol} \n\n <b>Action Required 🔔🔔</b>"
        )
        logging.error(f"END STREAM (Invalid Contract Address)- {address}!!!")
        return

    while True:
        events = filters.get_new_entries()
        if events:

            try:
                # res_data = client.get_buy_event_infura(Web3.toHex(events[0]['transactionHash']))
                # tx_hash = res_data['result']['hash']

                # data = client.get_tx_details(tx_hash, token_symbol=symbol)
                data = client.get_tx_details(
                    events[0]['transactionHash'], token_symbol=symbol)

                if data['buy_or_sell'] == 'buy':
                    logging.info(f"New Event!!! - {data}")
                    start_event(symbol, data, tg_link, icon)
                else:
                    logging.info("Not a valid Buy action")

            except Exception as e:
                logging.error(f"Please check & fix bug - {e}")


def start_event(symbol, event, tg_link, icon):
    "Send Buy Event To Group"
    file = open(f"{cwd}/sources.json")
    data = json.load(file)

    # channels = data['channels']
    # for chat in channels:
    bot.send_message(
        -1001553783220,
        f"<b>{event['name']} ({symbol})</b> Buy! \n{icon+icon+icon+icon+icon} \
            \n\n 💵 {event['price']} ETH (${event['usd_value']}) \
            \n 🪪 <a href='https://etherscan.io/address/{event['address']}'>{event['address'][:5]}...{event['address'][-4:]}</a> | Txn | Track \
            \n 🔘 Market Cap <b> ${event['market_cap']}</b> \
            \n\n <a href='https://dexscreener.com/ethereum/{event['contractAddress']}'>📊 Chart</a> <a href={tg_link}>📣 Telegram</a> <a href='https://app.uniswap.org/#/swap'>🤑Buy Now</a>",
        parse_mode="html",
        disable_web_page_preview=True
    )


def run():
    "Start Everything"

    file = open(f"{cwd}/sources.json")
    data = json.load(file)

    # pull token in models
    tokens = data['tokens']

    for token in tokens:
        symbol = token["symbol"]
        address = token["address"]

        # p = Process(target=start_streaming, name=token['symbol'], args=(token['symbol'], token['address']))
        # p.start()

        r = executor.submit(start_streaming, symbol,
                            address, "https//t.me/codefred", "🟢")
        print(r.done())
        active_pools[symbol] = r

        # p = threading.Thread(
        #     target=start_streaming, args=(token['symbol'], token['address']), name=token['symbol'])
        # p.start()
        # active_pools[symbol] = pool.apply_async(
        #     start_streaming, (symbol, address))
        # active_pools[symbol].get()


if __name__ == "__main__":
    run()
