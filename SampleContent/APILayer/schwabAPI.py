import requests
import json


class CharlesSchwabAPI:
    def __init__(self, client_id, client_secret, refresh_token):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.access_token = None
        self.refresh_access_token()

    def _get_headers(self):
        if not self.access_token:
            self.refresh_access_token()

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        return headers

    def _get_url(self, endpoint):
        return f'https://api.client.schwab.com{endpoint}'

    def _get_payload(self, data):
        return json.dumps(data)

    def refresh_access_token(self):
        data = {
            'grant_type': 'refresh_token',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token
        }

        response = requests.post('https://api.client.schwab.com/token', data=data)
        response.raise_for_status()

        self.access_token = response.json().get('access_token')

    def get_account_info(self):
        headers = self._get_headers()
        url = self._get_url('/accounts/v1/accounts')

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        return response.json()

    def get_account_value(self):
        headers = self._get_headers()
        url = self._get_url('/accounts/v1/accounts')

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        account_id = data['account'][0]['accountId']
        url = self._get_url(f'/accounts/v1/accounts/{account_id}/balances')

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        return float(data['positionsBalance']['marketValue'])

    def get_current_price(self, symbol):
        headers = self._get_headers()
        url = self._get_url(f'/market/symbol/{symbol}/fundamental')

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        return float(data['quote']['lastPrice'])

    def buy_stock(self, symbol, quantity, order_type='MARKET', price=None):
        headers = self._get_headers()
        url = self._get_url('/accounts/v1/accounts')

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        account_id = data['account'][0]['accountId']
        url = self._get_url(f'/accounts/v1/accounts/{account_id}/orders')

        if order_type == 'MARKET':
            order_type = 'MKT'
            price_type = None
        elif order_type == 'LIMIT':
            order_type = 'LMT'
            price_type = price
        else:
            raise ValueError(f'Invalid order type: {order_type}')

        data = {
            'orderType': order_type,
            'session': 'NORMAL',
            'duration': 'DAY',
            'orderStrategyType': 'SINGLE',
            'orderLegCollection': [
                {
                    'instruction': 'BUY',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': symbol,
                        'assetType': 'EQUITY'
                    },
                    'price': price_type
                }
            ]
        }

        payload = self._get_payload(data)
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()

        return response.json()

    def sell_stock(self, symbol, quantity, order_type='MARKET', price=None):
        headers = self._get_headers()
        url = self._get_url('/accounts/v1/accounts')

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        account_id = data['account'][0]['accountId']
        url = self._get_url(f'/accounts/v1/accounts/{account_id}/orders')

        if order_type == 'MARKET':
            order_type = 'MKT'
            price_type = None
        elif order_type == 'LIMIT':
            order_type = 'LMT'
            price_type = price
        else:
            raise ValueError(f'Invalid order type: {order_type}')

        data = {
            'orderType': order_type,
            'session': 'NORMAL',
            'duration': 'DAY',
            'orderStrategyType': 'SINGLE',
            'orderLegCollection': [
                {
                    'instruction': 'SELL',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': symbol,
                        'assetType': 'EQUITY'
                    },
                    'price': price_type
                }
            ]
        }

        payload = self._get_payload(data)
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()

        return response.json()
