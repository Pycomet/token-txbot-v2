import requests
import json
import time
import math
from config import *
from models import Token


def format_number(num):
    if num >= 1000000:
        return f"{num/1000000:.2f}M"
    elif num >= 1000:
        return f"{num/1000:.2f}K"
    else:
        return str(num)


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

    def get_buy_event_infura(self, tx):
        "Using infura mainets"
        # Set the parameters for the API call
        params = {
            "jsonrpc": "2.0",
            "method": "eth_getTransactionByHash",
            # Replace 0x123... with the transaction hash you want to retrieve
            "params": [tx],
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
        event_filter = self.contract.events.Transfer.createFilter(
            fromBlock='latest')
        return event_filter

    def get_token(self, address: str):
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

    def get_token_info(self, token_address):
        "Get Token Data"
        url = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2"

        query = """
            query getToken($token_address: String!) {
                token (id: $token_address) {
                    name
                    symbol
                    decimals
                    derivedETH
                    tradeVolumeUSD
                    totalLiquidity
                }
            }
        """

        # define the request headers
        headers = {
            "Content-Type": "application/json"
        }

        res = requests.post(url, json={"query": query, "variables": {
            "token_address": token_address.lower()
        }}, headers=headers)
        if res.status_code == 200:
            print(json.dumps(res.json(), indent=2))
            try:
                response = res.json()
                return response
            except:
                if response['errors']:
                    logging.error(
                        Exception(f"{response['errors'][0]['message']}"))
        else:
            logging.error(
                Exception(f"Query failed to run with a {res.status_code}."))

    def get_token_price_usd(self, token_address, eth_price):
        "Fetch The Token Price From Uniswap with GraphQl"
        response = self.get_token_info(token_address=token_address)

        eth_value = response['data']['token']['derivedETH']
        usd_value = float(eth_price) * float(eth_value)
        # Add name as extra export params
        return usd_value, response['data']['token']['name']

    def get_market_cap_usd(self, unit_value):
        "Get The USD Market Cap calue of the token"
        res = requests.get(
            f"https://api.ethplorer.io/getTokenInfo/{self.address}?apiKey=freekey")

        data = res.json()
        decimals = int(data['decimals'])
        total_supply = int(data['totalSupply'])

        def_res = float(total_supply) * float(unit_value)
        market_cap = def_res / math.pow(10, decimals)
        return "{:,.0f}".format(market_cap)

    def get_tx_details(self, tx_hash, token_symbol):
        # Send a GET request to the Ethereum API to retrieve the transaction details
        tx = web3_client.eth.getTransaction(tx_hash)
        # Extract the relevant details from the transaction
        # print(f"TEXTXTTX - {tx}")
        tx_details = {
            'price': round(tx['value'] / 1000000000000000000, 9),
            'gas_used': tx['gas'],
            'block_number': tx['blockNumber'],
            'timestamp': web3_client.eth.getBlock(tx['blockNumber'])['timestamp'],
            'tx_index': tx['transactionIndex'],
            'tx_hash': tx_hash,
            'address': tx['from'],
            'contractAddress': self.address
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

            price = cc.get_price('ETH', currency="USD")

            # Calculate the value of the transaction in ETH and USD
            eth_usd_price = price['ETH']['USD']
            value_eth = tx_details['price']
            value_usd = value_eth * float(eth_usd_price)

            unit_usd, _name = self.get_token_price_usd(
                token_address=self.address, eth_price=eth_usd_price)

            market_cap = self.get_market_cap_usd(unit_value=unit_usd)

            print(f"Market cap of the token in USD is: {market_cap}")
            tx_details['market_cap'] = market_cap
            tx_details['name'] = _name
            tx_details['token_symbol'] = token_symbol
            tx_details['eth_value'] = round(value_eth, 3)
            tx_details['usd_value'] = round(value_usd, 3)

        # Return the transaction details
        return tx_details

    def write_channel_to_json(self, name: str, id: str):
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
