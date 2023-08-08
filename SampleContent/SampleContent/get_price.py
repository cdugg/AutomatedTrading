import requests
import pandas as pd

key = '5A3SQY2IPZFVESQUNTXEOTMDVTNVRVAG'

def get_price_history(**kwargs):

    url = 'https://api.tdameritrade.com/v1/marketdata/{}/pricehistory'.format(kwargs.get('symbol'))

    params = {}
    params.update({'apikey': key})

    for arg in kwargs:
        parameter = {arg: kwargs.get(arg)}
        params.update(parameter)

    return requests.get(url, params=params).json()


def get_quotes(**kwargs):

    # Define endpoint URL
    url = 'https://api.tdameritrade.com/v1/marketdata/quotes'

    # Create parameters, update api key.
    params = {}
    params.update({'apikey': key})

    # Create and fill the symbol_list list with symbols from argument
    symbol_list = [symbol for symbol in kwargs.get('symbol')]
    params.update({'symbol': symbol_list})

    # Create request, with URL and parameters
    return requests.get(url, params=params).json()

def get_ohlc(**kwargs):
    data = get_quotes(symbol=kwargs.get('symbol'))
    for symbol in kwargs.get('symbol'):
        print(symbol)
        print(data[symbol]['openPrice'], data[symbol]['highPrice'], data[symbol]['lowPrice'], data[symbol]['lastPrice'])

print(pd.DataFrame(get_price_history(symbol='AAPL', period=1, periodType='day', frequencyType='minute')['candles']))
print(pd.DataFrame(get_quotes(symbol=['AAPL', 'AMD', 'TSLA'])))
get_ohlc(symbol=['AAPL', 'AMD', 'TSLA'])