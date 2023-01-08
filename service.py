import requests
import json
import time
from config import *
from models import Token

class APISource:

    def __init__(self, address, symbol) -> None:
        self.api_key = WEB3_API_KEY
        self.address = address
        self.symbol = symbol

    def get_hash_data(self, hash: str, input: str):
        "This uses etherscan to get the buy events on an address"
        # Retrieve the contract ABI for the smart contract
        contract_abi = [{
            "constant": False,
            "inputs": [
                {"name": "itemId", "type": "uint256"},
                {"name": "price", "type": "uint256"}
            ],
            "name": "buy",
            "outputs": [],
            "payable": True,
            "stateMutability": "payable",
            "type": "function"
        }]

        decoded_input = decode_abi(contract_abi, "buy", input)

        print(decoded_input)

        return 

    def is_buy_event(self, receipt: list):
        "Check if there is a buy event"
        for log in receipt:
            # Check if the log is a "buy" event
            if log['topics'][0] == web3_client.keccak(text="buy()"):
                return True
        return False

    def get_buy_event_infura(self, tx):
        "Using infura mainets"
        # Set the parameters for the API call
        params = {
            "jsonrpc": "2.0",
            "method": "eth_getTransactionByHash",
            "params": [tx],  # Replace 0x123... with the transaction hash you want to retrieve
            "id": 1,
        }

        # Send the request to the Infura API
        response = requests.post(NODE_PROVIDER, json=params)
        return response.json()

    def get_abi(self):
        "Fetch Token ABI from EtherScan API"

        result = requests.get(
            f"https://api.etherscan.io/api?module=contract&action=getabi&address={self.address}&apikey={self.api_key}",
        ).json()
        return result['result']

    def get_contract(self):
        "Fetch Contract Instance Address & ABI"
        try:
            # bytecode = web3_client.eth.getCode(self.address)
            # print(bytecode)
            self.abi = self.get_abi()
            addr = Web3.toChecksumAddress(self.address)
            self.contract = web3_client.eth.contract(
                address=addr,
                abi=self.abi
            )
            return self.contract
        except Exception as e:
            logging.error(f"Failed to Fetch Contract - {e}")
            return None

    def get_buy_events(self):
        "Returns An Event Filter For Buy Actions Only"
        # import pdb;
        # pdb.set_trace()
        event_filter = self.contract.events.Transfer.createFilter(fromBlock='latest')
        return event_filter
    

    def get_token(self, address:str):
        "Fetch Token ABI and symbol"
        # addr = Web3.isChecksumAddress(address)
        # abi = json.loads(self.get_abi())

        # contract = self.web3.eth.contract(address=address, abi=abi)
        # symbol = contract.functions.symbol().call()

        result = requests.get(
            f"https://api.coingecko.com/api/v3/coins/ethereum/contract/{address}",
        ).json()
        price_eth = result['market_data']['current_price']['eth']
        symbol = result['symbol']

        return price_eth, symbol.upper()


    def get_tx_details(self, tx_hash, token_symbol):
        # Send a GET request to the Ethereum API to retrieve the transaction details
        tx = web3_client.eth.getTransaction(tx_hash)
        # Extract the relevant details from the transaction
        tx_details = {
            'price': tx['value'] / 1000000000000000000,
            'gas_used': tx['gas'],
            'block_number': tx['blockNumber'],
            'timestamp': web3_client.eth.getBlock(tx['blockNumber'])['timestamp'],
            'tx_index': tx['transactionIndex'],
        }

        # Determine whether the transaction was a buy or a sell event
        if tx['value'] > 0:
            tx_details['buy_or_sell'] = 'buy'
        else:
            tx_details['buy_or_sell'] = 'sell'

        # Determine whether the recipient of the transaction was a new wallet owner
        if tx['to'] in web3_client.eth.accounts:
            tx_details['new_wallet_owner'] = False
        else:
            tx_details['new_wallet_owner'] = True


        # If the transaction was a buy event, retrieve the token name, value in ETH and USD, and market cap
        if tx_details['buy_or_sell'] == 'buy':
            # Retrieve the current price of ETH in USD
            r = requests.get('https://api.coinbase.com/v2/prices/ETH-USD/spot')
            eth_price_usd = r.json()['data']['amount']
            # Calculate the value of the transaction in ETH and USD
            value_eth = tx_details['price']
            value_usd = value_eth * float(eth_price_usd)
            # Retrieve the live market cap of the token
            # Get the total supply of the token
            total_supply = self.contract.functions.totalSupply().call()
            tx_details['token_symbol'] = token_symbol
            # Get the current exchange rate of the token in US dollars
            market_cap = ( total_supply * value_usd ) / tx['value']
            tx_details['market_cap'] = market_cap
            tx_details['eth_value'] = value_eth
            tx_details['usd_value'] = value_usd

        # Return the transaction details
        return tx_details

    
        

    def write_channel_to_json(self, name:str, id:str):
        "Write New Channel to Database"
        file = open(f'{cwd}/sources.json')
        data = json.load(file)

        # new channel
        data['channels'].append({
            'Group Name': name,
            'Group Id': id
        })
        with open(f'{cwd}/sources.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
            json_file.close()



