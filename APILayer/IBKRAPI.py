#Imports
import ibapi
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *
import numpy as np
import pandas as pd
import pytz
import math
from datetime import datetime, timedelta
import threading
import time
#Vars
ORDERID = 4

#Class for Interactive Brokers Connection
class IBApi(EWrapper,EClient):
    def __init__(self):
        EClient.__init__(self, self)

    # Get next order id we can use
    def incrementOrderID(self):
        global ORDERID
        ORDERID += 1


class InteractiveAPI:
    def __init__(self):
        self.orders = {}

    def connect(self):
        self.ib = IBApi()
        self.ib.connect("127.0.0.1", 7497, 1)
        ib_thread = threading.Thread(target=self.run_loop, daemon=True)
        ib_thread.start()
        time.sleep(1)

    def disconnect(self):
        self.ib.disconnect()

    def run_loop(self):
        self.ib.run()

    def create_contract(self, symbol, secType = "STK", exchange = "SMART", currency = "USD"):
        contract = Contract()
        contract.symbol = symbol
        contract.secType = secType
        contract.exchange = exchange
        contract.currency = currency
        return contract

    def create_market_order(self, action, quantity):
        order = Order()
        order.orderId = ORDERID
        order.orderType = "MKT"
        order.action = action
        order.totalQuantity = quantity
        order.eTradeOnly = ''
        order.firmQuoteOnly = ''
        self.orders[ORDERID] = set([order])
        self.ib.incrementOrderID()
        return ORDERID - 1, order

    def place_order(self, orderId, contract, order):
        self.ib.placeOrder(orderId, contract, order)
        self.orders[orderId].add(contract.symbol)

    def print_orders(self, placed=False):
        for id in self.orders.keys():
            if (len(self.orders[id]) > 1 and placed) or not placed:
                print(id, ": ", self.orders[id])
