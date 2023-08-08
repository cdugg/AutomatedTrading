import requests

class TDAmeritradeAPI:
    def __init__(self, client_id, redirect_uri, account_id, access_token):
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.account_id = account_id
        self.access_token = access_token
        self.base_url = 'https://api.tdameritrade.com/v1/'

    def _make_request(self, endpoint, method='GET', params=None, data=None):
        headers = {'Authorization': f'Bearer {self.access_token}'}
        url = self.base_url + endpoint

        if method == 'GET':
            response = requests.get(url, headers=headers, params=params)
        elif method == 'POST':
            response = requests.post(url, headers=headers, params=params, json=data)
        else:
            raise ValueError(f'Invalid HTTP method: {method}')

        response.raise_for_status()

        return response.json()

    def buy_stock(self, symbol, quantity, order_type='MARKET', price=None):
        endpoint = f'accounts/{self.account_id}/orders'

        if order_type == 'MARKET':
            order_data = {
                "orderType": "MARKET",
                "session": "NORMAL",
                "duration": "DAY",
                "orderStrategyType": "SINGLE",
                "orderLegCollection": [
                    {
                        "instruction": "Buy",
                        "quantity": quantity,
                        "instrument": {
                            "symbol": symbol,
                            "assetType": "EQUITY"
                        }
                    }
                ]
            }
        elif order_type == 'LIMIT':
            if price is None:
                raise ValueError('Price must be specified for LIMIT order')
            order_data = {
                "orderType": "LIMIT",
                "session": "NORMAL",
                "price": price,
                "duration": "DAY",
                "orderStrategyType": "SINGLE",
                "orderLegCollection": [
                    {
                        "instruction": "Buy",
                        "quantity": quantity,
                        "instrument": {
                            "symbol": symbol,
                            "assetType": "EQUITY"
                        }
                    }
                ]
            }
        else:
            raise ValueError(f'Invalid order type: {order_type}')

        response = self._make_request(endpoint, method='POST', data=order_data)

        return response


    def sell_stock(self, symbol, quantity, order_type='MARKET', price=None):
        endpoint = f'accounts/{self.account_id}/orders'

        if order_type == 'MARKET':
            order_data = {
                "orderType": "MARKET",
                "session": "NORMAL",
                "duration": "DAY",
                "orderStrategyType": "SINGLE",
                "orderLegCollection": [
                    {
                        "instruction": "Sell",
                        "quantity": quantity,
                        "instrument": {
                            "symbol": symbol,
                            "assetType": "EQUITY"
                        }
                    }
                ]
            }
        elif order_type == 'LIMIT':
            if price is None:
                raise ValueError('Price must be specified for LIMIT order')
            order_data = {
                "orderType": "LIMIT",
                "session": "NORMAL",
                "price": price,
                "duration": "DAY",
                "orderStrategyType": "SINGLE",
                "orderLegCollection": [
                    {
                        "instruction": "Sell",
                        "quantity": quantity,
                        "instrument": {
                            "symbol": symbol,
                            "assetType": "EQUITY"
                        }
                    }
                ]
            }
        else:
            raise ValueError(f'Invalid order type: {order_type}')

        response = self._make_request(endpoint, method='POST', data=order_data)

        return response


    def add_stop_loss(self, symbol, quantity, stop_price):
        endpoint = f'accounts/{self.account_id}/orders'

        data = {
            "orderType": "STOP",
            "session": "NORMAL",
            "duration": "DAY",
            "stopPrice": stop_price,
            "orderStrategyType": "SINGLE",
            "orderLegCollection": [
                {
                    "instruction": "Sell",
                    "quantity": quantity,
                    "instrument": {
                        "symbol": symbol,
                        "assetType": "EQUITY"
                    }
                }
            ]
        }

        response = self._make_request(endpoint, method='POST', data=data)

        return response

    def get_position_data(self):
        endpoint = f'accounts/{self.account_id}/positions'

        response = self._make_request(endpoint)

        return response

    def get_account_value(self):
        endpoint = f'accounts/{self.account_id}'

        params = {'fields': 'positions,orders,margin'}

        response = self._make_request(endpoint, params=params)

        return response['securitiesAccount']['currentBalances']['liquidationValue']

    def get_buying_power(self):
        endpoint = f'accounts/{self.account_id}'

        params = {'fields': 'positions,orders,margin'}

        response = self._make_request(endpoint, params=params)

        return response