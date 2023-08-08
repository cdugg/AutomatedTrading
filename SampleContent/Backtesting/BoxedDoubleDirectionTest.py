# Get historical data for 2004-Today

# Apply trade logic to it

# Check outcome and measure it with sharpe, percentage gain total, average daily percentage gain, total gain, etc

# Compare results with data from database

import datetime
import itertools
import time

import api
import mysql.connector
import pandas as pd
import pymysql
import requests
from pandas.io import sql
from sqlalchemy import create_engine


def open_long(price):
    pass

def close_long(price):
    pass

def open_short(price):
    pass

def close_short(price):
    pass

def trade(dataframe, long, short, trade_frequency):
    for _, line in dataframe.iterrows():
        value = line.iloc[2]
        if line.iloc[6].time() == datetime.time(9, 31, 0):
            print(f"Its 9:30 opening position at {value}")
            open_long(value)
            open_short(value)
            close_short_win_price = value - value * .01
            close_short_lose_price = value + value * .0025
            close_long_win_price = value + value * .01
            close_long_lose_price = value - value * .0025
        elif line.iloc[6].time() == datetime.time(16, 0, 0):
            close_long()
            close_short()
        else:
            pass
    return long, short, 0

def main():
    mindate = datetime.datetime(2021, 1, 1, 9, 0, 0, 0)
    middate = datetime.datetime(2022, 1, 1, 9, 0, 0, 0)
    twodate = datetime.datetime(2022, 1, 4, 9, 0, 0, 0)
    maxdate = datetime.datetime(2023, 1, 1, 9, 0, 0, 0)
    long = 25000
    short = 25000
    value_results = {}
    for ticker in api.TICKERS:
        data = api.pull_data("one_minute", [ticker], middate, twodate)[ticker]
        long, short, results = trade(data, long, short, "day")
        value_results[ticker] = results
        break
    print(value_results)

if __name__ == '__main__':
    main()