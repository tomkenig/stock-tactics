import requests
from datetime import datetime, date
import time
import pyodbc
import json
import pandas as pd
import pandas_ta as pta # https://mrjbq7.github.io/ta-lib/
import numpy as np
import talib as ta # install from whl file < https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
import btalib as bta # https://btalib.backtrader.com/introduction/


# binance data
# url_binance_data = 'https://api.binance.com/api/v3/klines?symbol='+market+'&interval='+tick_interval
# fear and greed
# url_fear_and_greed = 'https://api.alternative.me/fng/?limit=1000'

# settings
market = 'BTCUSDT'
tick_interval = '5m'
sql = "SELECT * FROM m1174_play.vw_klines_" + tick_interval + "_binance WHERE market = '" + market + "' and tick_interval = '" + tick_interval + "' and open_time/1000 >= 1577833200 order by open_time"
##  #where open_time/1000 >= 1624640865  # where open_time/1000 >= 1622567265 # 2020: 1577833200 #where open_time/1000 >= 1577833200

# print (sql)

# get ODBC connection string from stored file
with open('conf.json') as json_conf:
    SQL_DB_CONN_STRING = (json.load(json_conf))["connection_string"]

cnxn = pyodbc.connect(SQL_DB_CONN_STRING)
# cnxn.timeout = 4 # no timeout needed. Lots of data

df = pd.DataFrame(pd.read_sql_query(sql, con=cnxn))
cnxn.close()

# basics
df["open_time_dt"] = pd.to_datetime(df["open_time"], unit='ms')
df["open_time_yr"] = df["open_time_dt"].dt.year
df["open_time_mnt"] = df["open_time_dt"].dt.month
df["open_time_dy"] = df["open_time_dt"].dt.day

df["change_val"] = df.close - df.open
df["change_perc"] = df.close / df.open - 1
df["amplitude_val"] = df.high - df.low
df["amplitude_perc"] = df.high - df.low / df.open
df["up_down"] = np.where(df["close"] - df["close"].shift(1) > 0, 1, -1)

# token: trend up/down 1 / -1
# definition: in custom period sums of change are up or down.
# you an combine it with ADX - trend strength by multiply both ie. -1 * 40
df["token_change_7"] = df["change_val"].rolling(7).sum()
df["token_trend_7"] = np.where(df["token_change_7"] > 0, 1, -1)

df["token_change_14"] = df["change_val"].rolling(14).sum() # oryginal
df["token_trend_14"] = np.where(df["token_change_14"] > 0, 1, -1)

df["token_change_50"] = df["change_val"].rolling(50).sum()
df["token_trend_50"] = np.where(df["token_change_50"] > 0, 1, -1)

df["token_change_100"] = df["change_val"].rolling(100).sum()
df["token_trend_100"] = np.where(df["token_change_100"] > 0, 1, -1)


# indicators
# Moving averages
df["sma_7"] = pta.sma(df["close"], length=7)
df["sma_25"] = pta.sma(df["close"], length=25)
df["sma_99"] = pta.sma(df["close"], length=99)

df["wma_7"] = pta.wma(df["close"], length=7)
df["wma_25"] = pta.wma(df["close"], length=25)
df["wma_99"] = pta.wma(df["close"], length=99)

df["ema_7"] = pta.ema(df["close"], length=7)
df["ema_25"] = pta.ema(df["close"], length=25)
df["ema_99"] = pta.ema(df["close"], length=99)


# oscilators
# RSI
df["rsi_6"] = ta.RSI(df["close"], timeperiod=6) # tradingview corr, ok, checked
df["rsi_10"] = ta.RSI(df["close"], timeperiod=10) # tradingview corr, ok, checked
df["rsi_12"] = ta.RSI(df["close"], timeperiod=12) # tradingview corr, ok, checked
df["rsi_14"] = ta.RSI(df["close"], timeperiod=14) # tradingview corr, ok, checked
df["rsi_20"] = ta.RSI(df["close"], timeperiod=20) # tradingview corr, ok, checked
df["rsi_24"] = ta.RSI(df["close"], timeperiod=24) # tradingview corr, ok, checked

# Williams %R
df["will_perc_r_10"] = pta.willr(df["high"], df["low"], df["close"], 10) # tradingview corr
df["will_perc_r_14"] = pta.willr(df["high"], df["low"], df["close"], 14) # tradingview corr

# CCI
df["cci_14"] = pta.willr(df["high"], df["low"], df["close"], 14) # tradingview corr

# ROC - rate of change
df["roc_5"] = pta.roc(df["close"], 5)  # trandingview, ok, checked
df["roc_9"] = pta.roc(df["close"], 9)  # trandingview, ok, checked
df["roc_10"] = pta.roc(df["close"], 10)  # trandingview typical, ok, checked
df["roc_14"] = pta.roc(df["close"], 14)  # trandingview typical, ok, checked

# MFI - money flow index
df["mfi_7"] = pta.mfi(df["high"], df["low"], df["close"], df["volume"])  # trandingview, ok, checked
df["mfi_14"] = pta.mfi(df["high"], df["low"], df["close"], df["volume"])  # trandingview, ok, checked

# stoch - stochastic oscilator
df["stoch_slowk_5_3"], df["stoch_slowd_5_3"] = ta.STOCH(df["high"], df["low"], df["close"])  # ta-lib standard
df["stoch_fastk_5_3"], df["stoch_fastd_5_3"] = ta.STOCHF(df["high"], df["low"], df["close"])  # ta-lib standard

df["stoch_slowk_14_3"], df["stoch_slowd_14_3"] = ta.STOCH(df["high"], df["low"], df["close"])
df["stoch_fastk_14_3"], df["stoch_fastd_14_3"] = ta.STOCHF(df["high"], df["low"], df["close"], fastk_period=14)  # tradingview ok, checked

# StochRSI
#df["stoch_rsi"] = pta.sto

# ADX Average directional movement index
df["adx_7"] = ta.ADX(df["high"], df["low"], df["close"], timeperiod=7)
df["adx_14"] = ta.ADX(df["high"], df["low"], df["close"]) # standard
df["adx_50"] = ta.ADX(df["high"], df["low"], df["close"], timeperiod=50)
df["adx_100"] = ta.ADX(df["high"], df["low"], df["close"], timeperiod=100)


df["adxr_14"] = ta.ADXR(df["high"], df["low"], df["close"]) # standard



# token mod: Trend strength index
df["token_tsi_14"] = df["token_trend_14"] * df["adx_14"]


# volume indicators
# OBV - On Balance Volume
df["obv"] = pta.obv(df["close"], df["volume"])

# candles

df["cdl_doji"] = pta.cdl_doji(df["open"], df["high"], df["low"], df["close"])
df["cdl_dragonfly_doji"] = ta.CDLDRAGONFLYDOJI(df["open"], df["high"], df["low"], df["close"])
df["cdl_hammer"] = ta.CDLHAMMER(df["open"], df["high"], df["low"], df["close"])
df["cdl_marubozu"] = ta.CDLMARUBOZU(df["open"], df["high"], df["low"], df["close"])
df["cdl_longline"] = ta.CDLLONGLINE(df["open"], df["high"], df["low"], df["close"])
df["cdl_longlinedoji"] = ta.CDLLONGLEGGEDDOJI(df["open"], df["high"], df["low"], df["close"])
df["cdl_takuri"] = ta.CDLTAKURI(df["open"], df["high"], df["low"], df["close"])
df["cdl_3white_soldiers"] = ta.CDL3WHITESOLDIERS(df["open"], df["high"], df["low"], df["close"])


# combined token
# RSI rise 1 period
#df["rsi_6_rise_1_period"] = np.where(df["rsi_6"] > df["rsi_6"].shift(1), 1, 0)

# MFI raise 1 period
#df["mfi_7_rise_1_period"] = np.where(df["mfi_7"] > df["mfi_7"].shift(1), 1, 0)

# volume twice, two green after red
df["volume_twice_two_green_after_red"] = np.where((df["up_down"] == 1)
                                                  & (df["up_down"].shift(1) == 1)
                                                  & (df["up_down"].shift(2) == 0)
                                                  & (df["volume"] / df["volume"].shift(1) >= 1.2), 1, 0)

# TESTS strategies
# TESTS strategies
# TESTS strategies


test_stake = 100
test_indicator_buy_1 = "rsi_12"
#test_indicator_buy_2 = "token_trend_50"
#test_indicator_buy_3 = "token_trend_100"
#test_indicator_buy_4 = "adx_7"
test_indicator_value_1 = 15
#test_indicator_value_2 = 1
#test_indicator_value_3 = 1
#test_indicator_value_4 = 40
test_yield_expect = 0.03  # ie. 0.01=1%
test_wait_periods = 56  # ie. try to sell in next 6 periods (or 10)
test_stoploss = -0.008  # must be minus
test_stock_fee = -0.0015  # must be minus

df["tst_is_buy_signal"] = np.where((df[test_indicator_buy_1] < test_indicator_value_1)
#                                   & (df[test_indicator_buy_2] < test_indicator_value_2)
#                                   & (df[test_indicator_buy_3] < test_indicator_value_3)
#                                   & (df[test_indicator_buy_4] > test_indicator_value_4)
                                   , 1, 0)

df["tst_sell_price"] = df["close"] * test_yield_expect + df["close"]
df["tst_sell_stoploss_price"] = df["close"] + df["close"] * test_stoploss # must be plus
df["tst_high_in_sell_period"] = df["high"].rolling(test_wait_periods).max().shift(-test_wait_periods)
df["tst_low_in_sell_period"] = df["low"].rolling(test_wait_periods).min().shift(-test_wait_periods)
df["tst_sell_after_yield"] = np.where(df['tst_high_in_sell_period'] >= df["tst_sell_price"], 1, 0)
df["tst_sell_after_stoploss"] = np.where(df['tst_low_in_sell_period'] <= df["tst_sell_stoploss_price"], 1, 0)
df["tst_sold_price"] = np.where(df['tst_sell_after_yield'] == 1, df["tst_sell_price"], df["close"].shift(-1 * test_wait_periods)) # market after time
df["tst_sold_diff_perc"] = df["tst_sold_price"] / df["close"]
df["tst_single_game_result"] = np.where(df['tst_sold_diff_perc'] > 1, 1, -1)
df["tst_buy_sell_fee"] = test_stake * test_stock_fee # todo: change later, but accuracy is good
df["tst_single_game_earn"] = test_stake * df["tst_sold_diff_perc"] - test_stake
df["tst_single_game_earn_minus_fees"] = (test_stake * df["tst_sold_diff_perc"] - test_stake) + df["tst_buy_sell_fee"]
# todo: single game result with stoploss. Need improvement
df["tst_single_game_earn_minus_fees_with_stoploss"] = np.where(df['tst_sell_after_stoploss'] == 1 , test_stake * test_stoploss + df["tst_buy_sell_fee"], df["tst_single_game_earn_minus_fees"])


# test_name = "tst_" & market & "_" & tick_interval & "_" & test_indicator_buy_1

print(df.info(verbose=True))

# last check
#print(df)

# df2 aggr
df2 = df[df["tst_is_buy_signal"] == 1].groupby(["open_time_yr", "open_time_mnt"]).\
    aggregate({"tst_is_buy_signal": "sum",
               #"tst_single_game_earn": "sum",
               "tst_single_game_earn_minus_fees": "sum"
               #"tst_single_game_earn_minus_fees_with_stoploss": "sum"
               })

print(df2)

df3 = df[df["tst_is_buy_signal"] == 1].groupby(["open_time_yr"]).\
    aggregate({"tst_is_buy_signal": "sum",
               #"tst_single_game_earn": "sum",
               "tst_single_game_earn_minus_fees": "sum"
               #"tst_single_game_earn_minus_fees_with_stoploss": "sum"
               })

print(df3)

# save test results into database
# df2.to_excel("exports/export_" + market + "_" + tick_interval + "_" + str(time.time()) + ".xlsx")



# df.to_excel("exports/export_" + market + "_" + tick_interval + "_" + str(time.time()) + ".xlsx")


