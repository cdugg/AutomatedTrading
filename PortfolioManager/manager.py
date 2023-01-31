# Determine amount of money to contribute to a trade
# Never allow any account to trade if it will put the account value at risk of going below $25,000
# Based on trust level of Model used commit different amounts to trade
# Use corresponding APIs to the account being used

# To test apis being set up lets try to send one order to each client
# Buy 1 share of something cheap
import sys
sys.path.append('../')
from APILayer import IBKRAPI

IBKR = IBKRAPI.InteractiveAPI()
IBKR.connect()
contract = IBKR.create_contract("AAPL")
id, order = IBKR.create_market_order("BUY", 1)
id, order = IBKR.create_market_order("BUY", 2)
IBKR.place_order(id, contract, order)
print("All")
IBKR.print_orders()
print("Placed")
IBKR.print_orders(True)
IBKR.disconnect()