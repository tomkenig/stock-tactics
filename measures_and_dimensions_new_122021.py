# todo: update and lock records
# todo: zero-devide error in data frame
"""
pip install mysql-connector-python
pip install pandas
pip install numpy
"""
# libs
# import datetime
from db_works import db_connect, db_tables
import pandas as pd
import numpy as np
import pandas_ta as pta  # https://mrjbq7.github.io/ta-lib/
import talib as ta  # install from whl file < https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
import json
import time
import uuid  # https://docs.python.org/3/library/uuid.html
import openpyxl

db_schema_name, db_table_name, db_settings_table_name = db_tables()
cursor, cnxn = db_connect()

# todo: not need to use all params. just use download_settings_id
# todo: combination table. Can be stored in other schema

download_settings_id = 3
market = 'BTCUSDT'
tick_interval = '15m'
data_granulation = 'klines'
stock_type = 'spot'
stock_exchange = 'Binance.com'
open_time = str(1631042226) + '000'
print("select done settings done")
TACTICS_PACK_SIZE = 500000


# download OHLC data from DWH
def get_ohlc_data():
    cursor.execute("SELECT * FROM " + db_schema_name + ".vw_binance_klines_anl where market = '" + market + "' and "
                                     "tick_interval = '" + tick_interval + "' and "
                                     "data_granulation = '" + data_granulation + "' and "
                                     "stock_type = '" + stock_type + "' and "
                                     "open_time >= '" + open_time + "' and "
                                     "stock_exchange = '" + stock_exchange + "' ")
    df = pd.DataFrame(cursor.fetchall())
    df_bak = df.copy()  # absolutly needed. Simple assignment doesn't work
    print("OHLC data ready")
    return df, df_bak

df, df_bak = get_ohlc_data()
print(df)


def get_tactics_to_check():
    cursor.execute(
        "SELECT tactic_id, download_settings_id, test_stake, buy_indicator_1_name, buy_indicator_1_value, yield_expected, wait_periods "
        "FROM " + db_schema_name + ".vw_tactics_tests_to_analyse where tactic_status_id = 0 and download_settings_id = " + str(
            download_settings_id) + " limit " + str(TACTICS_PACK_SIZE) + " ")
    tactics_data = cursor.fetchall()
    return tactics_data


tactics_data = get_tactics_to_check()



def get_structured_data():
    df.columns = ["open_time",
                  "open",
                  "high",
                  "low",
                  "close",
                  "volume",
                  "close_time",
                  "quote_asset_volume",
                  "number_of_trades",
                  "taker_buy_base_asset_volume",
                  "taker_buy_quote_asset_volume",
                  "ignore",
                  "market",
                  "tick_interval",
                  "data_granulation",
                  "stock_type",
                  "stock_exchange",
                  "download_settings_id",
                  "insert_timestamp",
                  "open_datetime",
                  "close_datetime"]

get_structured_data()
print(df)



def get_indicators_basics():
    # basics
    df["open_time_dt"] = pd.to_datetime(df["open_datetime"], unit='ms')
    df["open_time_yr"] = df["open_time_dt"].dt.year
    df["open_time_mnt"] = df["open_time_dt"].dt.month
    df["open_time_dy"] = df["open_time_dt"].dt.day

    df["change_val"] = df.close - df.open
    df["change_perc"] = df.close / df.open - 1
    df["amplitude_val"] = df.high - df.low
    df["amplitude_perc"] = df.high - df.low / df.open
    df["up_down"] = np.where(df["close"] - df["close"].shift(1) > 0, 1, -1)


get_indicators_basics()
print(df)