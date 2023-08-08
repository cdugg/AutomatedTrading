import mysql.connector
import pandas as pd
import datetime

TICKERS = ["AAPL", "TSLA", "AMZN", "KO", "MCD", "SPY", "AMD", "F", "NVDA", "BAC", "T", "GOOG", "SHOP", "AAL", "GM", "PFE", "C", "EA", "PCG", "CCL"]

def pull_data(db, tickers=TICKERS, lower_date=datetime.datetime(2022, 1, 3, 9, 0, 0, 0), upper_date=datetime.datetime(2022, 1, 4, 9, 0, 0, 0)):
    """Pull all data between the given time ranges for each stock and return dictionary of the resulting tables for each."""
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        auth_plugin='mysql_native_password',
        database=db
    )
    cursor = mydb.cursor(buffered=True)
    results = {}
    for ticker in tickers:
        sql = f"""SELECT * FROM {ticker} WHERE time > '{lower_date}' AND time < '{upper_date}' ORDER BY time asc"""
        cursor.execute(sql)
        results[ticker] = pd.DataFrame(cursor.fetchall())
    return results