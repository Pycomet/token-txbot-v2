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
                start_event(symbol, events[0])


if __name__ == "__main__":
    run()