from SampleWatchlist import SampleWatchlist
import time

class SampleModelA:
    def __init__(self, broker=BrokerAPI(), watchlist=SampleWatchlist(), interval=5):
        if broker == 0:
            self.broker = broker
        # Stocks to monitor for this trading model
        self.watchlist = watchlist
        # Interval in seconds for which to request new data for watchlist
        self.interval = interval
        # Buy and sell lists to be updated every interval
        self.buy = []
        self.sell = []
        # Orders to execute at interval
        self.execute = []

    def monitor(self):
        self.buy_condition()
        self.sell_condition()
        if len(self.buy) > 0:
            self.create_buy_orders()
            self.buy = []
        if len(self.sell) > 0:
            self.create_sell_orders()
            self.sell = []
        time.sleep(self.interval)
    
    def buy_condition(self):
        # Check current watchlist values and return buy order if conditions are met
        self.watchlist.check_all()
        for symbol in self.watchlist.watchlist:
            if symbol.bid == 1:
                self.buy.append(symbol)

    def sell_condition(self):
        # Check current watchlist values and return sell order if conditions are met
        self.watchlist.check_all()
        for symbol in self.watchlist.watchlist:
            if symbol.ask == 2:
                self.sell.append(symbol)

    def create_buy_orders(self):
        if self.broker == 0:
            for item in self.buy:
                buy_order = self.broker.create_limit_buy()
                self.execute.append(buy_order)

    def create_sell_orders(self):
        if self.broker == 0:
            for item in self.sell:
                sell_order = self.broker.create_limit_sell()
                self.execute.append(sell_order)