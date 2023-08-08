# Determine amount of money to contribute to a trade
# Never allow any account to trade if it will put the account value at risk of going below $25,000
# Based on trust level of Model used commit different amounts to trade
# Use corresponding APIs to the account being used

# To test apis being set up lets try to send one order to each client
# Buy 1 share of something cheap
import sys
sys.path.append('../')
# from APILayer.IBKR import IBKRAPI

# IBKR = IBKRAPI.InteractiveAPI()
# IBKR.connect()
# contract = IBKR.create_contract("AAPL")
# id, order = IBKR.create_market_order("BUY", 1)
# id, order = IBKR.create_market_order("BUY", 2)
# IBKR.place_order(id, contract, order)
# print("All")
# IBKR.print_orders()
# print("Placed")
# IBKR.print_orders(True)
# IBKR.disconnect()


# Create OAuth connection to Ameritrade Application
from tda import auth, client
import json

token_path = 'token.json'
api_key = '5A3SQY2IPZFVESQUNTXEOTMDVTNVRVAG'
redirect_uri = 'http://localhost/test'
try:
    connection = auth.client_from_token_file(token_path, api_key)
except FileNotFoundError:
    from selenium import webdriver
    with webdriver.Chrome() as driver:
        connection = auth.client_from_login_flow(
            driver, api_key, redirect_uri, token_path)



# Get Accounts linked to login credentials provided
account_info = connection.get_accounts(fields=None)
assert account_info.status_code == 200, account_info.raise_for_status()
account_info = account_info.json()

print("Account ID:", account_info[0]['securitiesAccount']['accountId'])
accountId = account_info[0]['securitiesAccount']['accountId']
print("Value:", account_info[0]['securitiesAccount']['currentBalances']['liquidationValue'])
accountId = account_info[0]['securitiesAccount']['currentBalances']['liquidationValue']
print("Available Funds:", account_info[0]['securitiesAccount']['currentBalances']['cashAvailableForTrading'])
accountId = account_info[0]['securitiesAccount']['currentBalances']['cashAvailableForTrading']