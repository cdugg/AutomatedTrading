from schwabAPI import CharlesSchwabAPI
from ameritradeAPI import TDAmeritradeAPI
from IBKRAPI import InteractiveBrokersAPI

# Set up API credentials
schwab_client_id = 'your_client_id'
schwab_access_token = 'your_access_token'
td_client_id = 'your_client_id'
td_refresh_token = 'your_refresh_token'
ibkr_client_id = 'your_client_id'
ibkr_access_token = 'your_access_token'

# Set up account details
schwab_account_number = 'your_account_number'
td_account_number = 'your_account_number'
ibkr_account_number = 'your_account_number'

# Set up test variables
symbol = 'AAPL'
quantity = 10
order_type = 'LIMIT'
price = 150.0

# Initialize API classes
schwab_api = CharlesSchwabAPI(schwab_client_id, schwab_access_token)
td_api = TDAmeritradeAPI(td_client_id, td_refresh_token)
ibkr_api = InteractiveBrokersAPI(ibkr_client_id, ibkr_access_token)

# Test Charles Schwab API
schwab_api.authenticate()
print('Schwab Buying Power:', schwab_api.get_buying_power(schwab_account_number))
print('Schwab Account Info:', schwab_api.get_account_info(schwab_account_number))
schwab_api.buy_stock(symbol, quantity, order_type=order_type, price=price)
print('Schwab Positions:', schwab_api.get_positions(schwab_account_number))
schwab_api.sell_stock(symbol, quantity, order_type=order_type, price=price)
print('Schwab Positions:', schwab_api.get_positions(schwab_account_number))

# Test TD Ameritrade API
td_api.authenticate()
print('TD Ameritrade Buying Power:', td_api.get_buying_power(td_account_number))
print('TD Ameritrade Account Info:', td_api.get_account_info(td_account_number))
td_api.buy_stock(symbol, quantity, order_type=order_type, price=price)
print('TD Ameritrade Positions:', td_api.get_positions(td_account_number))
td_api.sell_stock(symbol, quantity, order_type=order_type, price=price)
print('TD Ameritrade Positions:', td_api.get_positions(td_account_number))

# Test Interactive Brokers API
ibkr_api.authenticate()
print('Interactive Brokers Buying Power:', ibkr_api.get_buying_power(ibkr_account_number))
print('Interactive Brokers Account Info:', ibkr_api.get_account_info(ibkr_account_number))
ibkr_api.buy_stock(symbol, quantity, order_type=order_type, price=price)
print('Interactive Brokers Positions:', ibkr_api.get_positions(ibkr_account_number))
ibkr_api.sell_stock(symbol, quantity, order_type=order_type, price=price)
print('Interactive Brokers Positions:', ibkr_api.get_positions(ibkr_account_number))
