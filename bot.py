from main import *
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
    for token in tokens:
        print(token["symbol"])
        print(token["address"])

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

                res_data = client.get_buy_event_infura(Web3.toHex(events[0]['transactionHash']))
                tx_hash = res_data['result']['hash']
                tx_input = res_data['result']['input']
                
                resp = web3_client.eth.getTransactionReceipt(tx_hash)['logs']

                data = client.get_tx_details(tx_hash, token_symbol=symbol)

                if data['buy_or_sell'] == 'buy':
                    print(data)
                    start_event(symbol, data)
                else:
                    print("Not a valid Buy action")


if __name__ == "__main__":
    run()