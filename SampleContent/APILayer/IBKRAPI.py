# #Imports
# import ibapi
# from ibapi.client import EClient
# from ibapi.wrapper import EWrapper
# from ibapi.contract import Contract
# from ibapi.order import *
# import numpy as np
# import pandas as pd
# import pytz
# import math
# from datetime import datetime, timedelta
# import threading
# import time
# #Vars
# ORDERID = 1

# #Class for Interactive Brokers Connection
# class IBApi(EWrapper,EClient):
#     def __init__(self):
#         EClient.__init__(self, self)

#     # Get next order id we can use
#     def incrementOrderID(self):
#         global ORDERID
#         ORDERID += 1


# class InteractiveAPI:
#     def __init__(self):
#         self.orders = {}

#     def connect(self):
#         self.ib = IBApi()
#         self.ib.connect("127.0.0.1", 7497, 1)
#         ib_thread = threading.Thread(target=self.run_loop, daemon=True)
#         ib_thread.start()
#         time.sleep(1)

#     def disconnect(self):
#         self.ib.disconnect()

#     def run_loop(self):
#         self.ib.run()

#     def create_contract(self, symbol, secType = "STK", exchange = "SMART", currency = "USD"):
#         contract = Contract()
#         contract.symbol = symbol
#         contract.secType = secType
#         contract.exchange = exchange
#         contract.currency = currency
#         return contract

#     def create_basic_order(self, action, order_type, quantity, tif=None, limit_price=None, discretionary_amount=None, aux_price=None):
#         order = Order()
#         order.orderId = ORDERID
#         order.orderType = order_type
#         order.action = action
#         order.totalQuantity = quantity
        

#         # ["MIT", "PEG MKT", "REL", "LIT", "PASSV REL", "PEG MID", "STP", "STP LMT", "STP PRT", "TRAIL", "TRAIL LIMIT"]
#         if not aux_price is None:
#             order.AuxPrice = aux_price
#         # ["AUC", "MKT", "LMT"] 
#         if not tif is None:
#             order.Tif = tif
#         # ["MTL", "LMT", "REL", "LIT", "LOC", "PEG MID", "STP LMT", "REL + LMT"]
#         if not limit_price is None:
#             order.LmtPrice = limit_price

#         order.eTradeOnly = ''
#         order.firmQuoteOnly = ''
#         self.orders[ORDERID] = set([order])
#         self.ib.incrementOrderID()
#         return ORDERID - 1, order

#     def place_order(self, orderId, contract, order):
#         self.ib.placeOrder(orderId, contract, order)
#         self.orders[orderId].add(contract.symbol)

#     def print_orders(self, placed=False):
#         for id in self.orders.keys():
#             if (len(self.orders[id]) > 1 and placed) or not placed:
#                 print(id, ": ", self.orders[id])
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order


class InteractiveBrokersClient(EClient):
    def __init__(self, wrapper):
        EClient.__init__(self, wrapper)


class InteractiveBrokersWrapper(EWrapper):
    def __init__(self):
        EWrapper.__init__(self)
        self.positions = {}
        self.account_value = 0
        self.buying_power = 0
        self.last_price = 0

    def position(self, account, contract, pos, avgCost):
        self.positions[contract.symbol] = {
            'position': pos,
            'average_cost': avgCost
        }

    def accountSummary(self, reqId, account, tag, value, currency):
        if tag == 'NetLiquidationByCurrency':
            self.account_value = float(value)

        if tag == 'BuyingPower':
            self.buying_power = float(value)

    def tickPrice(self, reqId, tickType, price, attrib):
        if tickType == 4:
            self.last_price = price


class InteractiveBrokersAPI:
    def __init__(self, host, port, client_id):
        self.host = host
        self.port = port
        self.client_id = client_id
        self.ib_client = InteractiveBrokersClient(InteractiveBrokersWrapper())
        self.ib_client.connect(host, port, client_id)

    def _get_contract(self, symbol):
        contract = Contract()
        contract.symbol = symbol
        contract.secType = 'STK'
        contract.exchange = 'SMART'
        contract.currency = 'USD'
        return contract

    def _get_order(self, quantity, order_type, price=None):
        order = Order()
        order.totalQuantity = quantity

        if order_type == 'MARKET':
            order.orderType = 'MKT'
        elif order_type == 'LIMIT':
            order.orderType = 'LMT'
            order.lmtPrice = price
        else:
            raise ValueError(f'Invalid order type: {order_type}')

        order.action = 'BUY'
        order.orderId = self.ib_client.nextOrderId()
        return order

    def get_position_data(self, symbol):
        contract = self._get_contract(symbol)
        self.ib_client.reqPositions()
        return self.ib_client.wrapper.positions.get(contract.symbol)

    def get_account_value(self):
        self.ib_client.reqAccountSummary(1, 'All', 'NetLiquidationByCurrency')
        return self.ib_client.wrapper.account_value

    def get_buying_power(self):
        self.ib_client.reqAccountSummary(1, 'All', 'BuyingPower')
        return self.ib_client.wrapper.buying_power

    def get_current_price(self, symbol):
        contract = self._get_contract(symbol)
        self.ib_client.reqMktData(1, contract, '', False, False, [])
        return self.ib_client.wrapper.last_price

    def buy_stock(self, symbol, quantity, order_type='MARKET', price=None):
        contract = self._get_contract(symbol)
        order = self._get_order(quantity, order_type, price)
        self.ib_client.placeOrder(order.orderId, contract, order)
        return order.orderId

    def sell_stock(self, symbol, quantity, order_type='MARKET', price=None):
        contract = self._get_contract(symbol)
        order = self._get_order(quantity, order_type, price)
        order.action = 'SELL'
        self.ib_client.placeOrder(order.orderId, contract, order)
        return order.orderId
