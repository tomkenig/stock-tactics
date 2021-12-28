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


def get_tactics_to_check():
    cursor.execute(
        "SELECT tactic_id, download_settings_id, test_stake, buy_indicator_1_name, buy_indicator_1_value, yield_expected, wait_periods "
        "FROM " + db_schema_name + ".vw_tactics_tests_to_analyse where tactic_status_id = 0 and download_settings_id = " + str(
            download_settings_id) + " limit " + str(TACTICS_PACK_SIZE) + " ")
    tactics_data = cursor.fetchall()
    return tactics_data


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


def get_indicators_trend_and_changes():
    # token: trend up/down 1 / -1
    # definition: in custom period sums of change are up or down.
    # you an combine it with ADX - trend strength by multiply both ie. -1 * 40
    df["token_change_7"] = df["change_val"].rolling(7).sum()
    df["token_trend_7"] = np.where(df["token_change_7"] > 0, 1, -1)
    df["token_change_14"] = df["change_val"].rolling(14).sum() # oryginal
    df["token_trend_14"] = np.where(df["token_change_14"] > 0, 1, -1)
    df["token_change_24"] = df["change_val"].rolling(24).sum()
    df["token_trend_24"] = np.where(df["token_change_24"] > 0, 1, -1)
    df["token_change_50"] = df["change_val"].rolling(50).sum()
    df["token_trend_50"] = np.where(df["token_change_50"] > 0, 1, -1)
    df["token_change_100"] = df["change_val"].rolling(100).sum()
    df["token_trend_100"] = np.where(df["token_change_100"] > 0, 1, -1)
    df["token_change_200"] = df["change_val"].rolling(200).sum()
    df["token_trend_200"] = np.where(df["token_change_200"] > 0, 1, -1)

def get_indicators_averages():
    # SMA (Simple)
    df["sma_7"] = pta.sma(df["close"], length=7)
    df["sma_14"] = pta.sma(df["close"], length=14)
    df["sma_25"] = pta.sma(df["close"], length=25)
    df["sma_50"] = pta.sma(df["close"], length=50)
    df["sma_99"] = pta.sma(df["close"], length=99)
    df["sma_100"] = pta.sma(df["close"], length=100)
    df["sma_200"] = pta.sma(df["close"], length=200)

    # SMA crosses
    # 1-fast higher than slow ; 2-fast lower than slow, 3 - cross period gold ; 4- cross period death
    df["sma_7_14_cross"] = np.where(((df["sma_7"] > df["sma_14"]) and (df["sma_7"].iloc[-1] < df["sma_14"].iloc[-1])), 1, 0)


    # WMA (Weighted)
    df["wma_7"] = pta.wma(df["close"], length=7)
    df["wma_14"] = pta.wma(df["close"], length=14)
    df["wma_25"] = pta.wma(df["close"], length=25)
    df["wma_50"] = pta.wma(df["close"], length=50)
    df["wma_99"] = pta.wma(df["close"], length=99)
    df["wma_100"] = pta.wma(df["close"], length=100)
    df["wma_200"] = pta.wma(df["close"], length=200)

    # EMA (Exponential)
    df["ema_7"] = pta.ema(df["close"], length=7)
    df["ema_14"] = pta.ema(df["close"], length=14)
    df["ema_25"] = pta.ema(df["close"], length=25)
    df["ema_50"] = pta.ema(df["close"], length=50)
    df["ema_99"] = pta.ema(df["close"], length=99)
    df["ema_100"] = pta.ema(df["close"], length=100)
    df["ema_200"] = pta.ema(df["close"], length=200)

    # MACD's
    # df["macd"] = ta.MACD



if __name__ == "__main__":
    df, df_bak = get_ohlc_data()
    print(df)

    tactics_data = get_tactics_to_check()

    get_structured_data()
    print(df)

    get_indicators_basics()
    print(df)

    get_indicators_trend_and_changes()
    print(df)

    get_indicators_averages()
    print(df)

#    df.to_excel("exports/export_" + market + "_" + tick_interval + "_" + str(time.time()) + ".xlsx")

